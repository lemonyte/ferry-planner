import { DurableObject } from "cloudflare:workers";
import type { SearchResult, Sort } from "./api";
import { type LocationId, locations, type TerminalId } from "./data/locations";
import { type Feed, parseFeed, Timetable } from "./gtfs";
import { type PlanOptions, routePlans } from "./route";
import { getSchedule, scheduleResponse, terminalCoordinates } from "./schedule";
import { findItinerary, selectItineraries } from "./search";
import { formatLocal, parseLocal, startOfDay, toLocal } from "./time";

const GTFS_URL = "https://data.trilliumtransit.com/gtfs/bcferries-bc-ca/bcferries-bc-ca.zip";
/** Time to wait before downloading the feed again after failing to, when there is no feed yet. */
const FEED_RETRY_MS = 60 * 1000;
/** Largest feed archive to read, many times the size of the feed. */
const MAX_FEED_BYTES = 20 * 1024 * 1024;
/** Longest buffer time in minutes, as longer ones only add to the work of finding no route plans. */
const MAX_BUFFER = 24 * 60;

const SORTS: Sort[] = ["duration", "departure", "arrival"];

/** Changed whenever the form of a stored feed is, so that one stored in another form is not taken for this one. */
const FEED_VERSION = 2;

interface StoredFeed {
    version: number;
    /** Version of the feed as given by the server it was downloaded from, to ask for the feed only if it has changed. */
    etag?: string;
    feed: Feed;
}

interface PlanRequest {
    origin: LocationId;
    destination: LocationId;
    options: PlanOptions;
}

/**
 * Keeps the BC Ferries feed and answers the requests that need it.
 *
 * There is a single planner, as the work it does takes more CPU time than a Worker gets on the Workers Free plan.
 */
export class Planner extends DurableObject<Env> {
    private etag?: string;
    private timetable?: Timetable;
    private loading?: Promise<void>;
    private retryAfter = 0;

    constructor(ctx: DurableObjectState, env: Env) {
        super(ctx, env);
        const stored = ctx.storage.kv.get<StoredFeed>("feed");
        if (stored?.version === FEED_VERSION) {
            this.etag = stored.etag;
            this.timetable = new Timetable(stored.feed);
        }
    }

    /** Download the feed if it has changed, and return whether it has. */
    async refresh(): Promise<boolean> {
        const response = await fetch(GTFS_URL, { headers: this.etag ? { "If-None-Match": this.etag } : {} });
        const etag = response.headers.get("ETag") ?? undefined;
        if (response.status === 304 || (etag && etag === this.etag)) {
            await response.body?.cancel();
            return false;
        }
        if (!response.ok) {
            throw new Error(`failed to download GTFS feed: status ${response.status}`);
        }
        if (Number(response.headers.get("Content-Length")) > MAX_FEED_BYTES) {
            throw new Error("failed to download GTFS feed: too large");
        }
        const feed = parseFeed(new Uint8Array(await response.arrayBuffer()), terminalCoordinates());
        if (feed.unserved.length > 0) {
            console.warn(
                JSON.stringify({
                    message: "no sailings in the GTFS feed for some terminals",
                    terminals: feed.unserved,
                }),
            );
        }
        // The previous feed stays in use if the new one cannot be stored.
        this.ctx.storage.kv.put<StoredFeed>("feed", { version: FEED_VERSION, etag, feed });
        this.etag = etag;
        this.timetable = new Timetable(feed);
        console.log(JSON.stringify({ message: "updated GTFS feed", etag, legs: feed.legs.length }));
        return true;
    }

    async fetch(request: Request): Promise<Response> {
        const { pathname, searchParams } = new URL(request.url);
        const parsed = parseRequest(
            request.method === "GET" ? parseQuery(searchParams) : await request.json().catch(() => undefined),
        );
        if (typeof parsed === "string") {
            return Response.json({ detail: parsed }, { status: 422 });
        }
        const { origin, destination, options } = parsed;
        const timetable = await this.getTimetable();
        if (pathname === "/api/ferry_schedule") {
            if (!timetable) {
                return Response.json({ detail: "Schedule not found" }, { status: 404 });
            }
            const schedule = getSchedule(timetable, origin as TerminalId, destination as TerminalId, options.date);
            return Response.json(scheduleResponse(schedule));
        }
        if (!timetable) {
            return Response.json({ detail: "Schedules are not available" }, { status: 503 });
        }
        const now = toLocal(Date.now());
        const plans = routePlans(origin, destination, options, timetable, now);
        if (pathname === "/api/routeplans") {
            return Response.json(plans);
        }
        if (pathname === "/api/itinerary") {
            const itinerary = findItinerary(plans, searchParams.get("id") ?? "");
            return itinerary
                ? Response.json(itinerary)
                : Response.json({ detail: "Itinerary not found" }, { status: 404 });
        }
        return Response.json({
            origin,
            destination,
            date: formatLocal(options.date).slice(0, 10),
            covered: timetable.covers(startOfDay(options.date)),
            now: formatLocal(now),
            ...selectItineraries(plans, formatLocal(now), {
                all: searchParams.get("routes") === "all",
                sort: SORTS.find((sort) => sort === searchParams.get("sort")),
                underway: searchParams.get("underway") === "true",
            }),
        } satisfies SearchResult);
    }

    private async getTimetable(): Promise<Timetable | undefined> {
        // There is only no feed before the first one has been downloaded, as it is kept from then on.
        if (!this.timetable && Date.now() >= this.retryAfter) {
            // Requests made in the meantime wait for the same download.
            this.loading ??= this.refresh()
                .then(() => undefined)
                .catch((error: unknown) => {
                    // Requests made in the next while do not each wait for another attempt.
                    this.retryAfter = Date.now() + FEED_RETRY_MS;
                    console.error(JSON.stringify({ message: "failed to get GTFS feed", error: String(error) }));
                })
                .finally(() => {
                    this.loading = undefined;
                });
            await this.loading;
        }
        return this.timetable;
    }
}

/** Read the body of a request, or say what is wrong with it. */
const parseRequest = (body: unknown): PlanRequest | string => {
    if (typeof body !== "object" || body === null || Array.isArray(body)) {
        return "request body must be a JSON object";
    }
    const { origin, destination, date, show_all, assured, hostled, buffer = 15 } = body as Record<string, unknown>;
    if (typeof origin !== "string" || !Object.hasOwn(locations, origin)) {
        return "origin is not a known location";
    }
    if (typeof destination !== "string" || !Object.hasOwn(locations, destination)) {
        return "destination is not a known location";
    }
    if (origin === destination) {
        return "origin and destination cannot be the same";
    }
    const time = date ? typeof date === "string" && parseLocal(date) : toLocal(Date.now());
    if (typeof time !== "number") {
        return "date is not a valid date";
    }
    if (typeof buffer !== "number" || !(buffer >= 0 && buffer <= MAX_BUFFER)) {
        return `buffer must be a number of minutes from 0 to ${MAX_BUFFER}`;
    }
    return {
        origin: origin as LocationId,
        destination: destination as LocationId,
        options: {
            date: time,
            showAll: show_all === true,
            assured: assured === true,
            hostled: hostled === true,
            buffer,
        },
    };
};

/** Read the query of a request the way its body would be, with text in place of what is not text. */
const parseQuery = (query: URLSearchParams): Record<string, unknown> => {
    const { show_all, assured, hostled, buffer, ...rest } = Object.fromEntries(query);
    return {
        ...rest,
        show_all: show_all === "true",
        assured: assured === "true",
        hostled: hostled === "true",
        buffer: buffer === undefined ? undefined : Number(buffer),
    };
};
