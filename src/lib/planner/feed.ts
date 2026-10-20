import { type Feed, parseFeed, Timetable } from "./gtfs.ts";
import { terminalCoordinates } from "./schedule.ts";

/** Same-origin proxy for the BC Ferries feed, which browsers cannot fetch cross-origin. */
export const FEED_URL = "/feed.zip";
const FEED_KEY = "ferry-planner:feed";
const CHECKED_KEY = "ferry-planner:feed-checked";
/** Minimum time between checks for a changed feed. */
const CHECK_INTERVAL_MS = 60 * 60 * 1000;
/** Time to wait before retrying a failed download. */
const FEED_RETRY_MS = 60 * 1000;
/** Maximum size of a feed archive. */
const MAX_FEED_BYTES = 20 * 1024 * 1024;

/** Increment when the `StoredFeed` format changes, so that feeds stored in the old format are discarded. */
const FEED_VERSION = 2;

interface StoredFeed {
    version: number;
    /** ETag of the feed, sent with later requests to download the feed only if it changed. */
    etag?: string;
    /** Epoch milliseconds when the feed was downloaded. */
    fetchedAt: number;
    feed: Feed;
}

/** Storage for the feed between visits. `localStorage` in a browser. */
export type FeedStorage = Pick<Storage, "getItem" | "setItem">;

/**
 * Downloads the BC Ferries feed, and downloads it again when it changes.
 *
 * The feed is stored so that it is available on the next visit, including offline.
 */
export class FeedKeeper {
    timetable?: Timetable;
    /** Epoch milliseconds when the feed was last checked for changes, or downloaded if it was never checked. */
    checkedAt?: number;
    private etag?: string;
    /** Epoch milliseconds before which the feed is not requested again. */
    private checkAfter = 0;
    /** Whether the last download failed. A failed download is retried sooner than the check interval. */
    private failed = false;
    private refreshing?: Promise<boolean>;

    constructor(private readonly storage?: FeedStorage) {
        const stored = this.read<StoredFeed>(FEED_KEY);
        // Storage can hold a feed in an older format.
        if (stored?.version === FEED_VERSION) {
            this.etag = stored.etag;
            this.checkedAt = Number(this.read(CHECKED_KEY)) || stored.fetchedAt;
            this.timetable = new Timetable(stored.feed);
            this.checkAfter = this.checkedAt + CHECK_INTERVAL_MS;
        }
    }

    /**
     * Download the feed if it has changed. Returns whether it changed.
     *
     * Skips the request within an hour of the last check, or within a minute of a failed download,
     * unless `retry` is set after a failure, such as when the connection returns.
     */
    refresh(retry = false): Promise<boolean> {
        if (Date.now() < this.checkAfter && !(retry && this.failed)) {
            return Promise.resolve(false);
        }
        // Concurrent callers share one download.
        this.refreshing ??= this.download().finally(() => {
            this.refreshing = undefined;
        });
        return this.refreshing;
    }

    /** Get the timetable, downloading the feed first if there is none. */
    async getTimetable(): Promise<Timetable | undefined> {
        if (!this.timetable) {
            await this.refresh().catch((error: unknown) => {
                console.error("failed to get GTFS feed", error);
            });
        }
        return this.timetable;
    }

    private async download(): Promise<boolean> {
        try {
            const changed = await this.fetchFeed();
            this.failed = false;
            this.checkedAt = Date.now();
            this.checkAfter = this.checkedAt + CHECK_INTERVAL_MS;
            this.write(CHECKED_KEY, this.checkedAt);
            return changed;
        } catch (error) {
            this.failed = true;
            this.checkAfter = Date.now() + FEED_RETRY_MS;
            throw error;
        }
    }

    private async fetchFeed(): Promise<boolean> {
        const response = await fetch(FEED_URL, { headers: this.etag ? { "If-None-Match": this.etag } : {} });
        const etag = response.headers.get("ETag") ?? undefined;
        if (response.status === 304) {
            await response.body?.cancel();
            return false;
        }
        if (!response.ok) {
            throw new Error(`failed to download GTFS feed: status ${response.status}`);
        }
        if (Number(response.headers.get("Content-Length")) > MAX_FEED_BYTES) {
            throw new Error("failed to download GTFS feed: too large");
        }
        const feed = parseFeed(new Uint8Array(await response.arrayBuffer()), terminalCoordinates());
        if (feed.unserved.length > 0) {
            console.warn("no sailings in the GTFS feed for some terminals", feed.unserved);
        }
        this.etag = etag;
        this.timetable = new Timetable(feed);
        // If storing fails, the feed is still used until the page closes.
        this.write(FEED_KEY, { version: FEED_VERSION, etag, fetchedAt: Date.now(), feed } satisfies StoredFeed);
        return true;
    }

    private read<Value>(key: string): Value | undefined {
        try {
            return JSON.parse(this.storage?.getItem(key) ?? "null") ?? undefined;
        } catch (error) {
            console.warn(`failed to read ${key} from storage`, error);
            return undefined;
        }
    }

    private write(key: string, value: unknown): void {
        try {
            this.storage?.setItem(key, JSON.stringify(value));
        } catch (error) {
            // Storage can be full or blocked, as in some private windows.
            console.warn(`failed to write ${key} to storage`, error);
        }
    }
}
