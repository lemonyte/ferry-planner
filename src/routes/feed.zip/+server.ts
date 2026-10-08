// Browsers are not let read the BC Ferries feed from the server that it is on, so they get it from here.
// The feed is passed on as it is, for the browser to read.

import { waitUntil } from "cloudflare:workers";
import type { RequestHandler } from "./$types";

const GTFS_URL = "https://data.trilliumtransit.com/gtfs/bcferries-bc-ca/bcferries-bc-ca.zip";
/** Time to keep the feed for before asking its server for it again. */
const CACHE_SECONDS = 60 * 60;

/** Get the cache of Cloudflare, which there is none of when developing. */
const getCache = (): Cache | undefined => {
    // Browsers have a cache by the same name, which is the one that the types know.
    return (globalThis as { caches?: { default?: Cache } }).caches?.default;
};

/** Read a version without the mark of being only alike, which is not told apart here. */
const bareEtag = (etag: string | null): string | undefined => {
    return etag?.replace(/^W\//, "");
};

export const GET: RequestHandler = async ({ request }) => {
    const cache = getCache();
    let feed = await cache?.match(GTFS_URL);
    if (!feed) {
        const response = await fetch(GTFS_URL).catch((error: unknown) => {
            console.error(
                JSON.stringify({ message: "failed to reach the server of the GTFS feed", error: String(error) }),
            );
        });
        if (!response?.ok) {
            await response?.body?.cancel();
            return new Response("The schedules are not available.", { status: 502 });
        }
        feed = new Response(response.body, {
            headers: {
                ETag: response.headers.get("ETag") ?? "",
                "Content-Type": "application/zip",
                "Cache-Control": `public, max-age=${CACHE_SECONDS}`,
            },
        });
        if (cache) {
            waitUntil(cache.put(GTFS_URL, feed.clone()));
        }
    }
    const etag = feed.headers.get("ETag");
    // The browser asks every time, and is only sent the feed when it has changed.
    const headers = { "Cache-Control": "no-cache", ...(etag ? { ETag: etag } : {}) };
    if (etag && bareEtag(request.headers.get("If-None-Match")) === bareEtag(etag)) {
        // Not waited for, as the copy that is being kept may still be read.
        void feed.body?.cancel();
        return new Response(null, { status: 304, headers });
    }
    return new Response(feed.body, { headers: { ...headers, "Content-Type": "application/zip" } });
};
