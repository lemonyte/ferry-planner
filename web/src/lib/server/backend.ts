import { env } from "cloudflare:workers";

/** Ask the backend Worker, which only this Worker can reach. */
export const fetchBackend = (path: string): Promise<Response> => {
    // Only the path matters, as the request goes straight to the Worker.
    return env.BACKEND.fetch(new URL(path, "https://backend"));
};
