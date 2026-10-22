import { DESCRIPTION, SITE_NAME } from "#lib/site.ts";

// Pages that are not prerendered get their title in the browser.
// Link previews do not run scripts, so the title and meta tags are injected on the server side.
const FALLBACK_HEAD = `<title>${SITE_NAME}</title>
        <meta property="og:title" content="${SITE_NAME}" />
        <meta property="og:description" content="${DESCRIPTION}" />
    `;

export const handle = async ({ event, resolve }) => {
    const response = await resolve(event, {
        transformPageChunk: ({ html }) => {
            return html.includes("<title>") ? html : html.replace("</head>", () => `${FALLBACK_HEAD}</head>`);
        },
    });
    // A trip belongs to one day, and its link stops working when the schedules change.
    if (event.route.id === "/trip/[id]") {
        response.headers.set("X-Robots-Tag", "noindex");
    }
    return response;
};
