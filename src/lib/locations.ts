import { type Location, type LocationId, locations } from "./planner/data/locations.ts";

export const placeName = (id: string): string => {
    return Object.hasOwn(locations, id) ? locations[id as LocationId].name : id;
};

/** Name a place without the "Terminal" suffix. */
export const shortName = (id: string): string => {
    return placeName(id).replace(/ \(?Terminal\)?$/, "");
};

/**
 * Find the places whose name or region contains `text`. Returns every place if `text` is empty.
 *
 * Sorted by match (name prefix, then name, then region), then by name.
 */
export const filterPlaces = (places: Record<string, Location>, text: string): Location[] => {
    const wanted = text.trim().toLowerCase();
    const rank = (place: Location): number => {
        const name = place.name.toLowerCase();
        if (name.startsWith(wanted)) {
            return 0;
        }
        if (name.includes(wanted)) {
            return 1;
        }
        return place.region.toLowerCase().includes(wanted) ? 2 : 3;
    };
    return Object.values(places)
        .filter((place) => rank(place) < 3)
        .sort((a, b) => rank(a) - rank(b) || a.name.localeCompare(b.name, "en"));
};
