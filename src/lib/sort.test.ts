import { expect, test } from "vitest";

import type { Itinerary } from "./planner/itinerary.ts";
import type { Query } from "./query.ts";
import { compareItineraries } from "./sort.ts";

const trip = (id: string, depart: string, arrive: string): Itinerary => {
    const [start, end] = [`2026-10-09T${depart}:00`, `2026-10-09T${arrive}:00`];
    return {
        id,
        route: "",
        depart: start,
        arrive: end,
        duration: (Date.parse(`${end}Z`) - Date.parse(`${start}Z`)) / 1000,
        drivingDistance: 0,
        mapUrl: "",
        steps: [],
    };
};

const TRIPS = [
    trip("early and slow", "06:00", "12:00"),
    trip("midday and fast", "10:00", "12:00"),
    trip("morning", "07:00", "10:30"),
    trip("late and fast", "15:00", "17:00"),
];

const order = (sort: Query["sort"]): string[] => {
    return TRIPS.toSorted(compareItineraries[sort]).map((itinerary) => itinerary.id);
};

test("duration sort puts the shortest trip first, then the earlier departure", () => {
    expect(order("duration")).toEqual(["midday and fast", "late and fast", "morning", "early and slow"]);
});

test("departure sort puts the earliest departure first", () => {
    expect(order("departure")).toEqual(["early and slow", "morning", "midday and fast", "late and fast"]);
});

test("arrival sort puts the earliest arrival first, then the later departure", () => {
    expect(order("arrival")).toEqual(["morning", "midday and fast", "early and slow", "late and fast"]);
});
