import { redirect } from "@sveltejs/kit";

// Prerendering a page that is not rendered on the server writes the bare app, which renders the page of
// whichever URL it is opened at. The service worker serves it offline for pages that are not prerendered.
export const prerender = true;

/** Runs only if this URL itself is opened. */
export const load = () => {
    redirect(307, "/");
};
