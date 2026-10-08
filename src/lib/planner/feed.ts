import { type Feed, parseFeed, Timetable } from "./gtfs";
import { terminalCoordinates } from "./schedule";

/** Where the BC Ferries feed is downloaded from, which is this site as browsers are not let read it from its own. */
export const FEED_URL = "/feed.zip";
const FEED_KEY = "ferry-planner:feed";
const CHECKED_KEY = "ferry-planner:feed-checked";
/** Time to leave between asking whether the feed has changed. */
const CHECK_INTERVAL_MS = 60 * 60 * 1000;
/** Time to wait before downloading the feed again after failing to. */
const FEED_RETRY_MS = 60 * 1000;
/** Largest feed archive to read, many times the size of the feed. */
const MAX_FEED_BYTES = 20 * 1024 * 1024;

/** Changed whenever the form of a stored feed is, so that one stored in another form is not taken for this one. */
const FEED_VERSION = 2;

interface StoredFeed {
    version: number;
    /** Version of the feed as given by the server it was downloaded from, to ask for the feed only if it has changed. */
    etag?: string;
    /** Instant that the feed was downloaded at. */
    fetchedAt: number;
    feed: Feed;
}

/** Where a feed is kept between visits, which is the local storage of a browser. */
export type FeedStorage = Pick<Storage, "getItem" | "setItem">;

/**
 * Keeps the BC Ferries feed, downloading it when there is none and again when it has changed.
 *
 * The feed is stored so that it is there the next time the page is opened, with or without a connection.
 */
export class FeedKeeper {
    timetable?: Timetable;
    /** Instant that the feed in use was downloaded at. */
    fetchedAt?: number;
    private etag?: string;
    /** Instant before which the feed is not asked for again. */
    private checkAfter = 0;
    /** Whether the last download failed, which is tried again sooner than a feed is checked for changes. */
    private failed = false;
    private refreshing?: Promise<boolean>;

    constructor(private readonly storage?: FeedStorage) {
        const stored = this.read<StoredFeed>(FEED_KEY);
        // Anything can be in storage, such as what an older version of the site left there.
        if (stored?.version === FEED_VERSION) {
            this.etag = stored.etag;
            this.fetchedAt = stored.fetchedAt;
            this.timetable = new Timetable(stored.feed);
            this.checkAfter = (Number(this.read(CHECKED_KEY)) || 0) + CHECK_INTERVAL_MS;
        }
    }

    /**
     * Download the feed if it has changed, and return whether it has.
     *
     * Nothing is asked of the server within the hour of the last time, or within a minute of failing to,
     * unless told to `retry` after a failure, as when a connection has come back.
     */
    refresh(retry = false): Promise<boolean> {
        if (Date.now() < this.checkAfter && !(retry && this.failed)) {
            return Promise.resolve(false);
        }
        // Whatever else asks in the meantime waits for the same download.
        this.refreshing ??= this.download().finally(() => {
            this.refreshing = undefined;
        });
        return this.refreshing;
    }

    /** Get the timetable of the feed, downloading the feed first when there is none yet. */
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
            this.checkAfter = Date.now() + CHECK_INTERVAL_MS;
            this.write(CHECKED_KEY, Date.now());
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
        if (response.status === 304 || (etag && etag === this.etag)) {
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
        this.fetchedAt = Date.now();
        this.timetable = new Timetable(feed);
        // The feed is still used for as long as the page is open if it cannot be stored.
        this.write(FEED_KEY, { version: FEED_VERSION, etag, fetchedAt: this.fetchedAt, feed } satisfies StoredFeed);
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
            // Storage can be full, or not allowed at all, as in some private windows.
            console.warn(`failed to write ${key} to storage`, error);
        }
    }
}
