import { describe, expect, it } from "vitest";

import { carConnections } from "./planner/data/car-connections.ts";
import { ferryConnections } from "./planner/data/ferry-connections.ts";
import type { LocationId } from "./planner/data/locations.ts";
import { findPopularRoute, POPULAR_ROUTES, routeSlug } from "./popular.ts";

describe("POPULAR_ROUTES", () => {
    it.each(POPULAR_ROUTES)("connects $from to $to by each of its ways", ({ from, to, ways }) => {
        expect(ways.length).toBeGreaterThan(0);
        for (const way of ways) {
            expect(way.length).toBeGreaterThan(0);
            // A drive joins two places unless they are the same terminal.
            const expectDrive = (origin: LocationId, destination: LocationId) => {
                if (origin !== destination) {
                    expect(
                        carConnections[origin]?.[destination],
                        `drive from ${origin} to ${destination}`,
                    ).toBeDefined();
                }
            };
            let place: LocationId = from;
            for (const [depart, arrive] of way) {
                expectDrive(place, depart);
                expect(ferryConnections[depart]?.[arrive], `sailing from ${depart} to ${arrive}`).toBeDefined();
                place = arrive;
            }
            expectDrive(place, to);
        }
    });

    it("has a route back for each route", () => {
        for (const { from, to } of POPULAR_ROUTES) {
            expect(findPopularRoute(routeSlug({ from: to, to: from })), `${to} to ${from}`).toBeDefined();
        }
    });

    it("has a different slug for each route", () => {
        const slugs = POPULAR_ROUTES.map(routeSlug);
        expect(new Set(slugs).size).toBe(slugs.length);
    });
});

describe("routeSlug", () => {
    it("joins the lowercase names of the places with hyphens", () => {
        expect(routeSlug({ from: "vancouver", to: "powell_river" })).toBe("vancouver-to-powell-river");
    });
});

describe("findPopularRoute", () => {
    it("finds a route by its slug", () => {
        expect(findPopularRoute("vancouver-to-victoria")).toMatchObject({ from: "vancouver", to: "victoria" });
    });

    it("returns `undefined` for a pair of places that is not a popular route", () => {
        expect(findPopularRoute("victoria-to-tofino")).toBeUndefined();
    });
});
