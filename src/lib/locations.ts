import { cities, terminals } from "./planner/data/locations";

/** City or ferry terminal that a journey can start or end at. */
export interface Place {
    id: string;
    name: string;
    region: string;
}

const toPlaces = (locations: Record<string, Place>): Place[] => {
    return Object.values(locations)
        .map(({ id, name, region }) => ({ id, name, region }))
        .sort((a, b) => (a.name < b.name ? -1 : 1));
};

export const CITIES = toPlaces(cities);
export const TERMINALS = toPlaces(terminals);

const NAMES = new Map([...CITIES, ...TERMINALS].map((place) => [place.id, place.name]));

export const placeName = (id: string): string => {
    return NAMES.get(id) ?? id;
};

/** Name a place without the word that marks it as a terminal, for where that is clear already. */
export const shortName = (id: string): string => {
    return placeName(id).replace(/ \(?Terminal\)?$/, "");
};

/** Find the places with some text in their name or region: names that start with it first, regions last. */
export const filterPlaces = (places: Place[], text: string): Place[] => {
    const wanted = text.trim().toLowerCase();
    if (!wanted) {
        return places;
    }
    const rank = (place: Place): number => {
        const name = place.name.toLowerCase();
        if (name.startsWith(wanted)) {
            return 0;
        }
        if (name.includes(wanted)) {
            return 1;
        }
        return place.region.toLowerCase().includes(wanted) ? 2 : 3;
    };
    // Sorting keeps places of the same rank in order of name.
    return places.filter((place) => rank(place) < 3).sort((a, b) => rank(a) - rank(b));
};
