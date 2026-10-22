// Caches the site so that it opens offline.
// The schedules are not cached here. The pages store them and request them from the network.

import { dev, version } from "$app/env";
import { assets, immutable, prerendered } from "$app/manifest";
import { self } from "$app/service-worker";

/** Includes the site version, so that the files of one version are never served to another. */
const CACHE = `site-${version}`;
/** App shell, served for every page without its own file. It renders the page from the URL. Prerendered by `src/routes/shell/`. */
const SHELL = "/shell";

const toPath = (path: string): string => {
    return new URL(path, self.registration.scope).pathname;
};

// Skip caching in development, where files change constantly.
// The share image is shown only in link previews, never by the site.
const FILES = dev
    ? []
    : [...immutable, ...assets, ...prerendered].map(({ path }) => toPath(path)).filter((path) => path !== "/og.png");
const KEPT = new Set(FILES);

self.addEventListener("install", (event) => {
    event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(FILES)));
});

// A new version waits until no page of the previous version is open, because such a page can still request its files.
self.addEventListener("activate", (event) => {
    event.waitUntil(
        (async () => {
            const names = await caches.keys();
            await Promise.all(names.filter((name) => name !== CACHE).map((name) => caches.delete(name)));
            // Also control the page that first installed this service worker.
            await self.clients.claim();
        })(),
    );
});

const respond = async (request: Request, path: string): Promise<Response> => {
    const cache = await caches.open(CACHE);
    return (await cache.match(path)) ?? fetch(request);
};

self.addEventListener("fetch", (event) => {
    const { request } = event;
    const url = new URL(request.url);
    if (dev || request.method !== "GET" || url.origin !== self.location.origin) {
        return;
    }
    if (KEPT.has(url.pathname)) {
        event.respondWith(respond(request, url.pathname));
    } else if (request.mode === "navigate") {
        event.respondWith(respond(request, SHELL));
    }
    // Other requests, such as the schedules, go to the network.
});
