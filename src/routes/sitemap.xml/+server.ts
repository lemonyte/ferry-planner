import { response } from "super-sitemap/sveltekit";

import { POPULAR_ROUTES, routeSlug } from "#lib/popular.ts";
import { ORIGIN } from "#lib/site.ts";

export const prerender = true;

export const GET = () => {
    return response({
        origin: ORIGIN,
        // The shell is the bare app for the service worker, and trips are only rendered in the browser.
        excludeRoutePatterns: [/^\/shell$/, /^\/trip\//],
        paramValues: {
            "/routes/[route]": POPULAR_ROUTES.map(routeSlug),
        },
    });
};
