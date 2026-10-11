// Proxy for the BC Ferries GTFS feed, which browsers cannot fetch cross-origin.
// The feed is passed through unmodified.

import { waitUntil } from "cloudflare:workers";

const GTFS_URL = "https://data.trilliumtransit.com/gtfs/bcferries-bc-ca/bcferries-bc-ca.zip";
/** Time to cache the feed before requesting it from its server again. */
const CACHE_SECONDS = 60 * 60;
/** Timeout for requests to the server of the feed. */
const TIMEOUT_MS = 20 * 1000;

/** Strip the weak validator prefix from an ETag, so that weak and strong ETags compare as equal. */
const bareEtag = (etag: string | null): string | undefined => {
    return etag?.replace(/^W\//, "");
};

/** Download the feed. Returns `undefined` if its server is unreachable or returns an error. */
const download = async (): Promise<Response | undefined> => {
    const response = await fetch(GTFS_URL, { signal: AbortSignal.timeout(TIMEOUT_MS) }).catch((error: unknown) => {
        console.error(JSON.stringify({ message: "failed to reach the server of the GTFS feed", error: String(error) }));
    });
    if (!response?.ok) {
        await response?.body?.cancel();
        return undefined;
    }
    const headers = new Headers({
        "Content-Type": "application/zip",
        "Cache-Control": `public, max-age=${CACHE_SECONDS}`,
    });
    const etag = response.headers.get("ETag");
    if (etag) {
        headers.set("ETag", etag);
    }
    return new Response(response.body, { headers });
};

export const GET = async ({ request }) => {
    // The DOM `CacheStorage` type shadows the Workers type, which has `default`.
    const cache = (caches as CacheStorage & { default: Cache }).default;
    let feed = await cache.match(GTFS_URL);
    if (!feed) {
        feed = await download();
        if (!feed) {
            return new Response("The schedules are not available.", { status: 502 });
        }
        waitUntil(cache.put(GTFS_URL, feed.clone()));
    }
    const etag = feed.headers.get("ETag");
    // The browser revalidates on every request and receives the feed only if it changed.
    const headers = { "Cache-Control": "no-cache", ...(etag ? { ETag: etag } : {}) };
    if (etag && bareEtag(request.headers.get("If-None-Match")) === bareEtag(etag)) {
        // Not awaited, because the clone being cached may still be read.
        void feed.body?.cancel();
        return new Response(null, { status: 304, headers });
    }
    return new Response(feed.body, { headers: { ...headers, "Content-Type": "application/zip" } });
};
