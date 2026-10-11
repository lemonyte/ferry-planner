import { expect, test } from "vitest";

import { filterPlaces, placeName, shortName } from "./locations.ts";
import { cities, terminals } from "./planner/data/locations.ts";

test("filterPlaces returns every place sorted by name for empty text", () => {
    const names = filterPlaces(cities, " ").map((place) => place.name);

    expect(names).toHaveLength(123);
    expect(names).toEqual(names.toSorted());
    expect(filterPlaces(terminals, "")).toHaveLength(50);
});

test("placeName returns the ID of an unknown place", () => {
    expect(placeName("atlantis")).toBe("atlantis");
    // An inherited `Object` property.
    expect(placeName("constructor")).toBe("constructor");
});

test("placeName returns the name of a place", () => {
    expect(placeName("van_anda")).toBe("Van Anda");
    expect(placeName("HSB")).toBe("Horseshoe Bay Terminal");
});

test("shortName omits the Terminal suffix", () => {
    expect(shortName("HSB")).toBe("Horseshoe Bay");
    expect(shortName("NBN")).toBe("New Brighton Dock");
    expect(shortName("vancouver")).toBe("Vancouver");
});

test("filterPlaces matches part of a name, ignoring case", () => {
    expect(filterPlaces(cities, "van and").map((place) => place.id)).toEqual(["van_anda"]);
});

test("filterPlaces matches the region", () => {
    expect(filterPlaces(cities, "texada").map((place) => place.id)).toContain("van_anda");
});

test("filterPlaces sorts name prefix matches first and region matches last", () => {
    const found = filterPlaces(cities, "van").map((place) => place.name);

    expect(found.slice(0, 5)).toEqual(["Van Anda", "Vancouver", "Vanderhoof", "North Vancouver", "West Vancouver"]);
    // Matches the Vancouver Island region.
    expect(found.indexOf("Alert Bay")).toBeGreaterThan(4);
});
