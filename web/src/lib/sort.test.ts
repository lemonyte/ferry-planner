import { expect, test } from "vitest";
import { sortItineraries } from "./sort";
import type { Itinerary } from "./types";

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

const order = (sort: Parameters<typeof sortItineraries>[1]): string[] => {
    return sortItineraries(TRIPS, sort).map((itinerary) => itinerary.id);
};

test("trips by duration have the shortest first, and the earlier of those as short as each other", () => {
    expect(order("duration")).toEqual(["midday and fast", "late and fast", "morning", "early and slow"]);
});

test("trips by departure have the one that leaves earliest first", () => {
    expect(order("departure")).toEqual(["early and slow", "morning", "midday and fast", "late and fast"]);
});

test("trips by arrival have the one that arrives earliest first, and the later to leave of those that arrive together", () => {
    expect(order("arrival")).toEqual(["morning", "midday and fast", "early and slow", "late and fast"]);
});

test("trips are left in the order that they came in", () => {
    const before = TRIPS.map((itinerary) => itinerary.id);

    sortItineraries(TRIPS, "duration");

    expect(TRIPS.map((itinerary) => itinerary.id)).toEqual(before);
});
