// Keeps the site itself in the browser, so that it opens without a connection.
// The schedules are not kept here: the pages keep those themselves, and ask for them past this.

import { dev, version } from "$app/env";
import { assets, immutable, prerendered, routes } from "$app/manifest";
import { self } from "$app/service-worker";

/** Named after the version of the site, so that the files of one version are never served to another. */
const CACHE = `site-${version}`;
/** The page that every page without a file of its own is, which finds what to show from its URL. */
const SHELL = "/";

const toPath = (path: string): string => {
    return new URL(path, self.registration.scope).pathname;
};

// Nothing is kept while developing, when the files change all the time.
const FILES = dev ? [] : [SHELL, ...[...immutable, ...assets, ...prerendered].map(({ path }) => toPath(path))];
const KEPT = new Set(FILES);
/** What the server answers itself, which is not a page even when a browser is sent to it. */
const ENDPOINTS = new Set(routes.filter((route) => route.endpoint && !route.page).map((route) => route.id as string));

self.addEventListener("install", (event) => {
    event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(FILES)));
});

// A new version waits until no page of the one before is open, which could still ask for the files of its own.
self.addEventListener("activate", (event) => {
    event.waitUntil(
        (async () => {
            const names = await caches.keys();
            await Promise.all(names.filter((name) => name !== CACHE).map((name) => caches.delete(name)));
            // The page that this was first installed by is served from here on as well.
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
    } else if (request.mode === "navigate" && !ENDPOINTS.has(url.pathname)) {
        event.respondWith(respond(request, SHELL));
    }
    // Anything else, such as the schedules, is left to the network.
});
