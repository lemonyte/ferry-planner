import { placeName } from "./locations.ts";
import type { LocationId, TerminalId } from "./planner/data/locations.ts";

/** A sailing, as its departure and arrival terminals. */
type Sailing = readonly [TerminalId, TerminalId];

/** A pair of places that has its own page. */
export interface PopularRoute {
    from: LocationId;
    to: LocationId;
    /** Ways to choose from, each as its sailings in order. */
    ways: readonly (readonly Sailing[])[];
}

export const POPULAR_ROUTES: readonly PopularRoute[] = [
    { from: "vancouver", to: "victoria", ways: [[["TSA", "SWB"]]] },
    { from: "victoria", to: "vancouver", ways: [[["SWB", "TSA"]]] },
    { from: "vancouver", to: "nanaimo", ways: [[["HSB", "NAN"]], [["TSA", "DUK"]]] },
    { from: "nanaimo", to: "vancouver", ways: [[["NAN", "HSB"]], [["DUK", "TSA"]]] },
    {
        from: "vancouver",
        to: "powell_river",
        ways: [
            [
                ["HSB", "LNG"],
                ["ERL", "SLT"],
            ],
            [
                ["HSB", "NAN"],
                ["CMX", "PWR"],
            ],
        ],
    },
    {
        from: "powell_river",
        to: "vancouver",
        ways: [
            [
                ["SLT", "ERL"],
                ["LNG", "HSB"],
            ],
            [
                ["PWR", "CMX"],
                ["NAN", "HSB"],
            ],
        ],
    },
    {
        from: "vancouver",
        to: "van_anda",
        ways: [
            [
                ["HSB", "LNG"],
                ["ERL", "SLT"],
                ["PWR", "TEX"],
            ],
            [
                ["HSB", "NAN"],
                ["CMX", "PWR"],
                ["PWR", "TEX"],
            ],
        ],
    },
    {
        from: "van_anda",
        to: "vancouver",
        ways: [
            [
                ["TEX", "PWR"],
                ["SLT", "ERL"],
                ["LNG", "HSB"],
            ],
            [
                ["TEX", "PWR"],
                ["PWR", "CMX"],
                ["NAN", "HSB"],
            ],
        ],
    },
];

/** Name a route in the path of its page, such as `vancouver-to-powell-river`. */
export const routeSlug = ({ from, to }: Pick<PopularRoute, "from" | "to">): string => {
    return `${placeName(from)} to ${placeName(to)}`.toLowerCase().replaceAll(" ", "-");
};

export const findPopularRoute = (slug: string): PopularRoute | undefined => {
    return POPULAR_ROUTES.find((route) => routeSlug(route) === slug);
};
