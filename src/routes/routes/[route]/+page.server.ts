import { error } from "@sveltejs/kit";

import { placeName } from "#lib/locations.ts";
import { carConnections } from "#lib/planner/data/car-connections.ts";
import { ferryConnections } from "#lib/planner/data/ferry-connections.ts";
import { type LocationId, type TerminalId, terminals } from "#lib/planner/data/locations.ts";
import { findPopularRoute, POPULAR_ROUTES, routeSlug } from "#lib/popular.ts";

// Loaded on the server so that the connection data stays out of the page that the browser downloads.
export const prerender = true;
export const ssr = true;

export const entries = () => {
    return POPULAR_ROUTES.map((route) => ({ route: routeSlug(route) }));
};

interface Drive {
    kind: "DRIVE";
    /** Names of the places. */
    from: string;
    to: string;
    seconds: number;
    kilometres: number;
}

interface Sailing {
    kind: "FERRY";
    depart: ReturnType<typeof getTerminal>;
    arrive: ReturnType<typeof getTerminal>;
    /** Minutes before the sailing that check-in closes with a reservation, if the sailing takes reservations. */
    reservationClose?: number;
}

/** Pick what the page shows of a terminal. */
const getTerminal = (id: TerminalId) => {
    const { name, info_url: infoUrl } = terminals[id];
    return { id, name, infoUrl };
};

/** Get the drive between two places. Returns no drive if they are the same terminal. */
const getDrives = (from: LocationId, to: LocationId): Drive[] => {
    if (from === to) {
        return [];
    }
    const drive = carConnections[from]?.[to];
    if (!drive) {
        throw new Error(`no drive from ${from} to ${to}`);
    }
    return [
        {
            kind: "DRIVE",
            from: placeName(from),
            to: placeName(to),
            seconds: drive.duration,
            kilometres: drive.distance,
        },
    ];
};

export const load = ({ params }) => {
    const route = findPopularRoute(params.route);
    if (!route) {
        error(404, "There is no page for this route.");
    }
    const { from, to } = route;
    return {
        slug: params.route,
        from: { id: from, name: placeName(from) },
        to: { id: to, name: placeName(to) },
        /** Each way as its drives and sailings in order. */
        ways: route.ways.map((way): (Drive | Sailing)[] => [
            // Each sailing is reached by a drive from the previous sailing, or from the start.
            ...way.flatMap(([depart, arrive], index): (Drive | Sailing)[] => [
                ...getDrives(way[index - 1]?.[1] ?? from, depart),
                {
                    kind: "FERRY",
                    depart: getTerminal(depart),
                    arrive: getTerminal(arrive),
                    reservationClose: ferryConnections[depart]?.[arrive]?.bookable
                        ? terminals[depart].res_close
                        : undefined,
                },
            ]),
            ...getDrives(way.at(-1)?.[1] ?? from, to),
        ]),
    };
};
