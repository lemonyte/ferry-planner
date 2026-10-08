// The schedules are a feed that the browser downloads and keeps, and that all the searches of a visit are made with.

import { FeedKeeper } from "#lib/planner/feed.ts";
import { toLocal } from "#lib/planner/time.ts";
import type { Query } from "#lib/query.ts";
import type { Itinerary, SearchResult } from "#lib/types.ts";
import { browser } from "$app/env";
import { invalidate } from "$app/navigation";

/** What the pages made from the schedules depend on, to be made again when the schedules have changed. */
export const SCHEDULES = "schedules:current";

export interface Planner {
    /** Find the trips worth taking for a search, or nothing if it is not between two places that are known. */
    search: (query: Query) => SearchResult | undefined;
    /** Find the trip of a search with an ID. */
    itinerary: (query: Query, id: string) => Itinerary | undefined;
}

/** What there is to say about the schedules, once the page is in a browser. */
export const schedules = $state<{
    /** Instant that the schedules in use were downloaded at, if there are any. */
    fetchedAt?: number;
    online: boolean;
}>({ online: true });

const getStorage = (): Storage | undefined => {
    try {
        return localStorage;
    } catch {
        // Even asking for the storage fails where it is not allowed.
        return undefined;
    }
};

let keeper: FeedKeeper | undefined;

const getKeeper = (): FeedKeeper => {
    // There is nothing stored where a page is made ahead of time.
    keeper ??= new FeedKeeper(browser ? getStorage() : undefined);
    return keeper;
};

/** Check if there are schedules already, so that a search does not have to wait for them. */
export const hasSchedules = (): boolean => {
    return getKeeper().timetable !== undefined;
};

/**
 * Get what searches are made with, or nothing if there are no schedules and none can be downloaded.
 *
 * The planner and the connections that it goes by are only loaded when first asked for.
 */
export const getPlanner = async (): Promise<Planner | undefined> => {
    const [timetable, planner] = await Promise.all([getKeeper().getTimetable(), import("#lib/planner/plan.ts")]);
    schedules.fetchedAt = getKeeper().fetchedAt;
    return (
        timetable && {
            search: (query) => planner.search(query, timetable, toLocal(Date.now())),
            itinerary: (query, id) => planner.itinerary(query, id, timetable, toLocal(Date.now())),
        }
    );
};

const refresh = async (retry = false): Promise<void> => {
    const keeper = getKeeper();
    const replaces = keeper.timetable !== undefined;
    try {
        const changed = await keeper.refresh(retry);
        schedules.fetchedAt = keeper.fetchedAt;
        // What is shown was made with the schedules that these replace.
        if (changed && replaces) {
            await invalidate(SCHEDULES);
        }
    } catch (error) {
        // The schedules there already are stay in use.
        console.error("failed to refresh the schedules", error);
    }
};

/**
 * Keep the schedules up to date for as long as the page is open, and return a function that stops doing so.
 *
 * They are checked when the page is opened or come back to, and when a connection comes back.
 */
export const watchSchedules = (): (() => void) => {
    const stop = new AbortController();
    const setOnline = () => {
        schedules.online = navigator.onLine;
    };
    setOnline();
    schedules.fetchedAt = getKeeper().fetchedAt;
    window.addEventListener("offline", setOnline, stop);
    window.addEventListener(
        "online",
        () => {
            setOnline();
            void refresh(true);
        },
        stop,
    );
    document.addEventListener(
        "visibilitychange",
        () => {
            if (document.visibilityState === "visible") {
                void refresh();
            }
        },
        stop,
    );
    void refresh();
    return () => stop.abort();
};
