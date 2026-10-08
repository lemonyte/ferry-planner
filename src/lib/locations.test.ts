import { expect, test } from "vitest";
import { CITIES, filterPlaces, placeName, shortName, TERMINALS } from "./locations";

test("places are every city and terminal, in order of name", () => {
    expect(CITIES).toHaveLength(123);
    expect(TERMINALS).toHaveLength(50);
    expect(CITIES.map((place) => place.name)).toEqual(CITIES.map((place) => place.name).toSorted());
});

test("place is named by its ID", () => {
    expect(placeName("van_anda")).toBe("Van Anda");
    expect(placeName("HSB")).toBe("Horseshoe Bay Terminal");
});

test("terminal is named in short without the word", () => {
    expect(shortName("HSB")).toBe("Horseshoe Bay");
    expect(shortName("NBN")).toBe("New Brighton Dock");
    expect(shortName("vancouver")).toBe("Vancouver");
});

test("places are found by part of their name, whatever its case", () => {
    expect(filterPlaces(CITIES, "van and").map((place) => place.id)).toEqual(["van_anda"]);
});

test("places are found by their region", () => {
    expect(filterPlaces(CITIES, "texada").map((place) => place.id)).toContain("van_anda");
});

test("places whose name starts with what was typed come first, and those only in a region with it last", () => {
    const found = filterPlaces(CITIES, "van").map((place) => place.name);

    expect(found.slice(0, 5)).toEqual(["Van Anda", "Vancouver", "Vanderhoof", "North Vancouver", "West Vancouver"]);
    // In the region of Vancouver Island.
    expect(found.indexOf("Alert Bay")).toBeGreaterThan(4);
});

test("every place is found when nothing is typed", () => {
    expect(filterPlaces(TERMINALS, " ")).toEqual(TERMINALS);
});
