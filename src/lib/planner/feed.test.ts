import { afterEach, beforeEach, expect, type MockInstance, test, vi } from "vitest";

import { type FeedFiles, makeArchive } from "#test/feeds.ts";

import { FEED_URL, FeedKeeper } from "./feed.ts";

const BOTH_WAYS: FeedFiles = {
    trips: "r,daily,t\nr,daily,u\n",
    stopTimes: "t,07:30:00,07:30:00,1,1\nt,08:10:00,08:10:00,2,2\nu,09:00:00,09:00:00,2,1\nu,09:40:00,09:40:00,1,2\n",
};
const DAY = Date.UTC(2026, 9, 6);
const NOON = Date.UTC(2026, 9, 6, 12);
const MINUTE = 60 * 1000;
const HOUR = 60 * MINUTE;

type Body = Uint8Array | string;
type Content = Body | number | { body: Body; etag: string };

/** In-memory stand-in for `localStorage`. */
class MemoryStorage {
    readonly items = new Map<string, string>();

    getItem(key: string): string | null {
        return this.items.get(key) ?? null;
    }

    setItem(key: string, value: string): void {
        this.items.set(key, value);
    }
}

let now: MockInstance<() => number>;

beforeEach(() => {
    now = vi.spyOn(Date, "now").mockReturnValue(NOON);
    vi.spyOn(console, "error").mockImplementation(() => undefined);
    vi.spyOn(console, "warn").mockImplementation(() => undefined);
});

afterEach(() => {
    vi.restoreAllMocks();
});

/** Copy an archive into a valid `Response` body. */
const toBody = (body?: Body): string | Uint8Array<ArrayBuffer> | undefined => {
    return typeof body === "object" ? new Uint8Array(body) : body;
};

/** Mock `fetch` to return the given archives or statuses in order, repeating the last. */
const serve = (...contents: Content[]) => {
    return vi.spyOn(globalThis, "fetch").mockImplementation(async () => {
        const content = contents.length > 1 ? contents.shift() : contents[0];
        // Lets concurrent callers request the feed during the download.
        await new Promise((resolve) => setTimeout(resolve, 1));
        if (typeof content === "number") {
            return new Response(null, { status: content });
        }
        return typeof content === "object" && "etag" in content
            ? new Response(toBody(content.body), { headers: { ETag: content.etag } })
            : new Response(toBody(content));
    });
};

const sailings = async (keeper: FeedKeeper, origin: string, destination: string): Promise<number | undefined> => {
    return (await keeper.getTimetable())?.sailings(origin, destination, DAY).length;
};

test("concurrent callers share one feed download", async () => {
    const fetch = serve(makeArchive());
    const keeper = new FeedKeeper(new MemoryStorage());

    const found = await Promise.all([sailings(keeper, "HSB", "LNG"), sailings(keeper, "LNG", "HSB")]);
    found.push(await sailings(keeper, "HSB", "LNG"));

    expect(found).toEqual([1, 0, 1]);
    expect(fetch).toHaveBeenCalledTimes(1);
    expect(fetch).toHaveBeenCalledWith(FEED_URL, { headers: {} });
});

test("feed is stored for the next visit", async () => {
    const fetch = serve(makeArchive());
    const storage = new MemoryStorage();
    await new FeedKeeper(storage).getTimetable();

    const keeper = new FeedKeeper(storage);

    expect(keeper.timetable?.sailings("HSB", "LNG", DAY)).toHaveLength(1);
    expect(keeper.checkedAt).toBe(NOON);
    expect(fetch).toHaveBeenCalledTimes(1);
});

test.each([
    ["in an older format", (stored: string) => JSON.stringify({ ...JSON.parse(stored), version: 1 })],
    ["that is not valid JSON", () => "{"],
    ["that is null", () => "null"],
])("stored feed %s is downloaded again", async (_, change) => {
    const fetch = serve({ body: makeArchive(), etag: '"first"' });
    const storage = new MemoryStorage();
    await new FeedKeeper(storage).getTimetable();
    for (const [key, value] of storage.items) {
        storage.items.set(key, change(value));
    }

    const keeper = new FeedKeeper(storage);

    expect(keeper.timetable).toBeUndefined();
    expect(await sailings(keeper, "HSB", "LNG")).toBe(1);
    expect(fetch).toHaveBeenCalledTimes(2);
    expect(fetch).toHaveBeenLastCalledWith(FEED_URL, { headers: {} });
});

test.each([
    ["cannot be downloaded", 503],
    ["is not a GTFS archive", "<html>Waiting room</html>"],
    // The stop sequences are missing.
    ["is malformed", makeArchive({ stopTimes: "t,07:30:00,07:30:00,1\nt,08:10:00,08:10:00,2\n" })],
])("getTimetable returns undefined if the feed %s", async (_, content) => {
    serve(content);

    expect(await new FeedKeeper(new MemoryStorage()).getTimetable()).toBeUndefined();
});

test("getTimetable returns undefined if the feed exceeds the size limit", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
        new Response(toBody(makeArchive()), { headers: { "Content-Length": String(21 * 1024 * 1024) } }),
    );

    expect(await new FeedKeeper(new MemoryStorage()).getTimetable()).toBeUndefined();
});

test("concurrent callers share one failed download", async () => {
    const fetch = serve(503);
    const keeper = new FeedKeeper(new MemoryStorage());

    const found = await Promise.all([keeper.getTimetable(), keeper.getTimetable()]);
    found.push(await keeper.getTimetable());

    expect(found).toEqual([undefined, undefined, undefined]);
    expect(fetch).toHaveBeenCalledTimes(1);
});

test("failed download is retried after one minute", async () => {
    serve(503, makeArchive());
    const keeper = new FeedKeeper(new MemoryStorage());
    expect(await keeper.getTimetable()).toBeUndefined();

    now.mockReturnValue(NOON + MINUTE + 1000);

    expect(await sailings(keeper, "HSB", "LNG")).toBe(1);
});

test("failed download is retried immediately if retry is set", async () => {
    serve(503, makeArchive());
    const keeper = new FeedKeeper(new MemoryStorage());
    expect(await keeper.getTimetable()).toBeUndefined();

    expect(await keeper.refresh(true)).toBe(true);

    expect(keeper.timetable).toBeDefined();
});

test("refresh replaces the feed if it changed", async () => {
    serve(makeArchive(), makeArchive(BOTH_WAYS));
    const storage = new MemoryStorage();
    const keeper = new FeedKeeper(storage);
    expect(await sailings(keeper, "LNG", "HSB")).toBe(0);

    now.mockReturnValue(NOON + HOUR);

    expect(await keeper.refresh()).toBe(true);
    expect(await sailings(keeper, "LNG", "HSB")).toBe(1);
    expect(keeper.checkedAt).toBe(NOON + HOUR);
    expect(new FeedKeeper(storage).timetable?.sailings("LNG", "HSB", DAY)).toHaveLength(1);
});

test("refresh does not request the feed again within an hour, including after a reload", async () => {
    const fetch = serve(makeArchive());
    const storage = new MemoryStorage();
    const keeper = new FeedKeeper(storage);
    expect(await keeper.refresh()).toBe(true);

    now.mockReturnValue(NOON + HOUR - 1000);

    expect(await keeper.refresh()).toBe(false);
    expect(await keeper.refresh(true)).toBe(false);
    expect(await new FeedKeeper(storage).refresh()).toBe(false);
    expect(fetch).toHaveBeenCalledTimes(1);
});

test("refresh sends the ETag to download the feed only if it changed", async () => {
    const fetch = serve({ body: makeArchive(), etag: '"first"' }, 304);
    const storage = new MemoryStorage();
    const keeper = new FeedKeeper(storage);
    expect(await keeper.refresh()).toBe(true);

    now.mockReturnValue(NOON + HOUR);

    expect(await keeper.refresh()).toBe(false);
    expect(fetch).toHaveBeenLastCalledWith(FEED_URL, { headers: { "If-None-Match": '"first"' } });
    expect(keeper.timetable).toBeDefined();
    expect(keeper.checkedAt).toBe(NOON + HOUR);
    expect(new FeedKeeper(storage).checkedAt).toBe(NOON + HOUR);
    // The feed was unchanged, so the next check is an hour later.
    now.mockReturnValue(NOON + 2 * HOUR - 1000);
    expect(await keeper.refresh()).toBe(false);
    expect(fetch).toHaveBeenCalledTimes(2);
});

test("refresh sends the stored ETag after a reload", async () => {
    const fetch = serve({ body: makeArchive(), etag: '"first"' });
    const storage = new MemoryStorage();
    await new FeedKeeper(storage).refresh();

    now.mockReturnValue(NOON + HOUR);
    await new FeedKeeper(storage).refresh();

    expect(fetch).toHaveBeenLastCalledWith(FEED_URL, { headers: { "If-None-Match": '"first"' } });
});

test.each([
    ["cannot be downloaded", 503, "status 503"],
    ["is not a GTFS archive", "<html>Waiting room</html>", "invalid zip data"],
])("refresh rejects and keeps the previous feed if the feed %s", async (_, content, message) => {
    serve(makeArchive(), content);
    const keeper = new FeedKeeper(new MemoryStorage());
    await keeper.refresh();

    now.mockReturnValue(NOON + HOUR);

    await expect(keeper.refresh()).rejects.toThrow(message);
    expect(await sailings(keeper, "HSB", "LNG")).toBe(1);
});

test.each([
    [
        "cannot be stored",
        Object.assign(new MemoryStorage(), {
            setItem: () => {
                throw new DOMException("The quota has been exceeded.", "QuotaExceededError");
            },
        }),
    ],
    [
        "cannot be read from storage",
        Object.assign(new MemoryStorage(), {
            getItem: () => {
                throw new DOMException("The operation is insecure.", "SecurityError");
            },
        }),
    ],
    ["has no storage", undefined],
])("feed is used until the page closes if it %s", async (_, storage) => {
    serve(makeArchive());
    const keeper = new FeedKeeper(storage);

    expect(await sailings(keeper, "HSB", "LNG")).toBe(1);
    expect(await keeper.refresh()).toBe(false);
});
