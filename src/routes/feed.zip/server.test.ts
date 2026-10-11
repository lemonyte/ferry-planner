import { afterEach, expect, test, vi } from "vitest";

import { GET } from "./+server.ts";

const GTFS_URL = "https://data.trilliumtransit.com/gtfs/bcferries-bc-ca/bcferries-bc-ca.zip";

/** Promises passed to `waitUntil`. */
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

/** Mock `fetch` to return the given content, or a response with the given status. */
const serve = (content: string | number, etag = '"first"') => {
    return vi.spyOn(globalThis, "fetch").mockImplementation(async () => {
        return typeof content === "number"
            ? new Response(null, { status: content })
            : new Response(content, { headers: { ETag: etag, "Content-Type": "application/octet-stream" } });
    });
};

/** Stub `caches.default`. Returns its entries. */
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

test("feed is proxied with the ETag from its server", async () => {
    const fetch = serve("feed");
    makeCache();

    const response = await get();

    expect(response.status).toBe(200);
    expect(await response.text()).toBe("feed");
    expect(response.headers.get("ETag")).toBe('"first"');
    expect(response.headers.get("Content-Type")).toBe("application/zip");
    expect(response.headers.get("Cache-Control")).toBe("no-cache");
    expect(fetch).toHaveBeenCalledExactlyOnceWith(GTFS_URL, { signal: expect.any(AbortSignal) });
});

test("feed is cached for one hour", async () => {
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
    ["matches", '"first"'],
    ["matches except for the weak prefix", 'W/"first"'],
])("responds 304 if the If-None-Match ETag %s", async (_, etag) => {
    serve("feed");
    makeCache();

    const response = await get({ "If-None-Match": etag });

    expect(response.status).toBe(304);
    expect(await response.text()).toBe("");
    expect(response.headers.get("ETag")).toBe('"first"');
});

test("responds with the feed if the If-None-Match ETag differs", async () => {
    serve("feed", '"second"');
    makeCache();

    const response = await get({ "If-None-Match": '"first"' });

    expect(response.status).toBe(200);
    expect(await response.text()).toBe("feed");
});

test("feed without an ETag is proxied without one", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response("feed"));
    makeCache();

    const response = await get({ "If-None-Match": '"first"' });

    expect(response.status).toBe(200);
    expect(response.headers.has("ETag")).toBe(false);
});

test("responds 502 if the feed server returns an error", async () => {
    serve(503);
    const cached = makeCache();

    const response = await get();
    await Promise.all(pending);

    expect(response.status).toBe(502);
    expect(cached.size).toBe(0);
});

test("responds 502 if the feed server is unreachable", async () => {
    vi.spyOn(globalThis, "fetch").mockRejectedValue(new TypeError("fetch failed"));
    vi.spyOn(console, "error").mockImplementation(() => undefined);

    makeCache();

    expect((await get()).status).toBe(502);
});
