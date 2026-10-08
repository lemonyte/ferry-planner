import { expect, test } from "vitest";
import { carConnections } from "./data/car-connections";
import { ferryConnections } from "./data/ferry-connections";
import { cities, locations, terminals } from "./data/locations";

// These checks stand in for validating the data files every time the site starts.

test("locations are listed under their own ID", () => {
    for (const [id, location] of Object.entries(locations)) {
        expect(location.id).toBe(id);
    }
});

test("no city shares an ID with a terminal", () => {
    expect(Object.keys(locations)).toHaveLength(Object.keys(cities).length + Object.keys(terminals).length);
});

test("terminals have coordinates and are named as terminals", () => {
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

test("car connections join two different locations", () => {
    for (const [origin, destinations] of Object.entries(carConnections)) {
        expect(locations).toHaveProperty(origin);
        for (const [destination, connection] of Object.entries(destinations)) {
            expect(locations).toHaveProperty(destination);
            expect(destination).not.toBe(origin);
            // Courtenay and Comox Valley are listed as no distance apart.
            expect(connection.duration).toBeGreaterThanOrEqual(0);
            expect(connection.distance).toBeGreaterThanOrEqual(0);
            expect(connection.fuel).toBeGreaterThanOrEqual(0);
        }
    }
});

test("ferry connections join two different terminals", () => {
    for (const [origin, destinations] of Object.entries(ferryConnections)) {
        expect(terminals).toHaveProperty(origin);
        for (const destination of Object.keys(destinations)) {
            expect(terminals).toHaveProperty(destination);
            expect(destination).not.toBe(origin);
        }
    }
});

test("no two locations are joined by both car and ferry", () => {
    for (const [origin, destinations] of Object.entries(ferryConnections)) {
        for (const destination of Object.keys(destinations)) {
            expect(carConnections[origin as keyof typeof carConnections] ?? {}).not.toHaveProperty(destination);
        }
    }
});
