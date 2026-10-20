import { expect, test } from "vitest";

import { carConnections } from "./data/car-connections.ts";
import { carFuel } from "./data/car-fuel.ts";
import { ferryConnections } from "./data/ferry-connections.ts";
import { cities, locations, terminals } from "./data/locations.ts";
import { terminalDetails } from "./data/terminal-details.ts";

// These checks replace validating the data files at startup.

test("each location key matches its ID", () => {
    for (const [id, location] of Object.entries(locations)) {
        expect(location.id).toBe(id);
    }
});

test("no city shares an ID with a terminal", () => {
    expect(Object.keys(locations)).toHaveLength(Object.keys(cities).length + Object.keys(terminals).length);
});

test("terminals have valid coordinates and a terminal name", () => {
    for (const terminal of Object.values(terminals)) {
        const [latitude, longitude, ...rest] = terminal.coordinates.split(",").map(Number);
        expect(rest).toEqual([]);
        expect(latitude).toBeGreaterThan(48);
        expect(latitude).toBeLessThan(55);
        expect(longitude).toBeGreaterThan(-134);
        expect(longitude).toBeLessThan(-122);
        expect(terminal.name).toMatch(/terminal/i);
    }
});

test("car connections connect two different locations", () => {
    for (const [origin, destinations] of Object.entries(carConnections)) {
        expect(locations).toHaveProperty(origin);
        for (const [destination, connection] of Object.entries(destinations)) {
            expect(locations).toHaveProperty(destination);
            expect(destination).not.toBe(origin);
            // Courtenay and Comox Valley are 0 km apart.
            expect(connection.duration).toBeGreaterThanOrEqual(0);
            expect(connection.distance).toBeGreaterThanOrEqual(0);
        }
    }
});

test("each car connection has its fuel usage, and no other connection has one", () => {
    const keys = (connections: Record<string, Record<string, unknown> | undefined>) =>
        Object.entries(connections).flatMap(([origin, destinations]) =>
            Object.keys(destinations ?? {}).map((destination) => `${origin}-${destination}`),
        );
    expect(keys(carFuel)).toEqual(keys(carConnections));
    for (const fuel of Object.values(carFuel).flatMap((destinations) => Object.values(destinations ?? {}))) {
        expect(fuel).toBeGreaterThanOrEqual(0);
    }
});

test("each terminal has its details, and no other location has them", () => {
    expect(Object.keys(terminalDetails)).toEqual(Object.keys(terminals));
});

test("ferry connections connect two different terminals", () => {
    for (const [origin, destinations] of Object.entries(ferryConnections)) {
        expect(terminals).toHaveProperty(origin);
        for (const destination of Object.keys(destinations)) {
            expect(terminals).toHaveProperty(destination);
            expect(destination).not.toBe(origin);
        }
    }
});

test("no two locations are connected by both car and ferry", () => {
    for (const [origin, destinations] of Object.entries(ferryConnections)) {
        for (const destination of Object.keys(destinations)) {
            expect(carConnections[origin as keyof typeof carConnections] ?? {}).not.toHaveProperty(destination);
        }
    }
});
