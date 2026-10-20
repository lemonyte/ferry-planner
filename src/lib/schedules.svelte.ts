import { browser } from "$app/env";
import { invalidate } from "$app/navigation";

import { FeedKeeper } from "#lib/planner/feed.ts";
import type { Itinerary, SearchResult } from "#lib/planner/itinerary.ts";
import { toLocal } from "#lib/planner/time.ts";
import type { Query } from "#lib/query.ts";

/** Dependency key for `load` functions that use the schedules. Invalidated when the schedules change. */
export const SCHEDULES = "schedules:current";

export interface Planner {
    /** Find the trips to show for a search, or `undefined` if its places or date are not valid. */
    search: (query: Query) => SearchResult | undefined;
    /** Find a trip of a search by ID. */
    itinerary: (query: Query, id: string) => Itinerary | undefined;
}

/** State of the schedules, for display. */
export const schedules = $state<{
    /** Epoch milliseconds when the schedules were last checked for changes, if there are any schedules. */
    checkedAt?: number;
    online: boolean;
}>({ online: true });

const getStorage = (): Storage | undefined => {
    try {
        return localStorage;
    } catch {
        // Accessing `localStorage` throws if storage is blocked.
        return undefined;
    }
};

let keeper: FeedKeeper | undefined;
/** Whether a `load` function ran without schedules and must rerun when they arrive. */
let missed = false;

const getKeeper = (): FeedKeeper => {
    // Prerendering has no storage.
    keeper ??= new FeedKeeper(browser ? getStorage() : undefined);
    return keeper;
};

/** Check if the schedules are loaded, so that a search does not have to wait for a download. */
export const hasSchedules = (): boolean => {
    return getKeeper().timetable !== undefined;
};

/**
 * Get the planner, or `undefined` if there are no schedules and they cannot be downloaded.
 *
 * The planner and its connection data are loaded on first use.
 */
export const getPlanner = async (): Promise<Planner | undefined> => {
    const [timetable, planner] = await Promise.all([getKeeper().getTimetable(), import("#lib/planner/plan.ts")]);
    schedules.checkedAt = getKeeper().checkedAt;
    missed ||= timetable === undefined;
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
        schedules.checkedAt = keeper.checkedAt;
        // The page was rendered with the previous schedules, or without any.
        if (changed && (replaces || missed)) {
            missed = false;
            await invalidate(SCHEDULES);
        }
    } catch (error) {
        // The existing schedules stay in use.
        console.error("failed to refresh the schedules", error);
    }
};

/**
 * Keep the schedules up to date while the page is open. Returns a function that stops the updates.
 *
 * Checks when the page opens, becomes visible, or comes back online.
 */
export const watchSchedules = (): (() => void) => {
    const stop = new AbortController();
    const setOnline = () => {
        schedules.online = navigator.onLine;
    };
    setOnline();
    schedules.checkedAt = getKeeper().checkedAt;
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
