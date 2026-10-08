import { afterEach, expect, test, vi } from "vitest";
import { GET } from "./+server.ts";

const GTFS_URL = "https://data.trilliumtransit.com/gtfs/bcferries-bc-ca/bcferries-bc-ca.zip";

/** What was left to finish after the responses. */
const pending = vi.hoisted((): Promise<unknown>[] => []);

vi.mock("cloudflare:workers", () => ({
    waitUntil: (promise: Promise<unknown>) => {
        pending.push(promise);
    },
}));

afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
    pending.length = 0;
});

/** Answer each download of the feed with what is given, or with the status given. */
const serve = (content: string | number, etag = '"first"') => {
    return vi.spyOn(globalThis, "fetch").mockImplementation(async () => {
        return typeof content === "number"
            ? new Response(null, { status: content })
            : new Response(content, { headers: { ETag: etag, "Content-Type": "application/octet-stream" } });
    });
};

/** Put a cache where Cloudflare has its own, and return what is kept in it. */
const makeCache = (): Map<string, Response> => {
    const cached = new Map<string, Response>();
    vi.stubGlobal("caches", {
        default: {
            match: async (key: string) => cached.get(key)?.clone(),
            put: async (key: string, response: Response) => {
                cached.set(key, response);
            },
        },
    });
    return cached;
};

const get = (headers: Record<string, string> = {}): Promise<Response> => {
    const event = { request: new Request("https://site/feed.zip", { headers }) };
    return Promise.resolve(GET(event as unknown as Parameters<typeof GET>[0]));
};

test("feed is passed on with the version that its server gives it", async () => {
    const fetch = serve("feed");
    makeCache();

    const response = await get();

    expect(response.status).toBe(200);
    expect(await response.text()).toBe("feed");
    expect(response.headers.get("ETag")).toBe('"first"');
    expect(response.headers.get("Content-Type")).toBe("application/zip");
    expect(response.headers.get("Cache-Control")).toBe("no-cache");
    expect(fetch).toHaveBeenCalledExactlyOnceWith(GTFS_URL);
});

test("feed is downloaded once for the requests of an hour", async () => {
    const fetch = serve("feed");
    const cached = makeCache();
    await (await get()).text();
    await Promise.all(pending);

    const response = await get();

    expect(await response.text()).toBe("feed");
    expect(response.headers.get("ETag")).toBe('"first"');
    expect(fetch).toHaveBeenCalledTimes(1);
    expect(cached.get(GTFS_URL)?.headers.get("Cache-Control")).toBe("public, max-age=3600");
});

test.each([
    ["the same", '"first"'],
    ["the same but for how alike it is said to be", 'W/"first"'],
])("feed is not sent again to a browser whose version of it is %s", async (_, etag) => {
    serve("feed");
    makeCache();

    const response = await get({ "If-None-Match": etag });

    expect(response.status).toBe(304);
    expect(await response.text()).toBe("");
    expect(response.headers.get("ETag")).toBe('"first"');
});

test("feed is sent to a browser that has another version of it", async () => {
    serve("feed", '"second"');
    makeCache();

    const response = await get({ "If-None-Match": '"first"' });

    expect(response.status).toBe(200);
    expect(await response.text()).toBe("feed");
});

test("feed is passed on where there is no cache, as when developing", async () => {
    serve("feed");

    expect(await (await get()).text()).toBe("feed");
});

test("no feed when its server does not give it", async () => {
    serve(503);
    const cached = makeCache();

    const response = await get();
    await Promise.all(pending);

    expect(response.status).toBe(502);
    expect(cached.size).toBe(0);
});

test("no feed when its server cannot be reached", async () => {
    vi.spyOn(globalThis, "fetch").mockRejectedValue(new TypeError("fetch failed"));
    vi.spyOn(console, "error").mockImplementation(() => undefined);

    makeCache();

    expect((await get()).status).toBe(502);
});
