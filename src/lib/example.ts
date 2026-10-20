import type { Itinerary } from "./planner/itinerary.ts";

/** Trip shown on the home page as an example of a result. Its times are made up. */
export const EXAMPLE_TRIP: Itinerary = {
    id: "example",
    route: "vancouver-HSB-LNG-ERL-SLT-powell_river",
    depart: "2026-01-01T08:40:00",
    arrive: "2026-01-01T14:17:00",
    duration: 20160,
    drivingDistance: 139,
    mapUrl: "",
    steps: [
        {
            kind: "DRIVE",
            start: "2026-01-01T08:40:00",
            end: "2026-01-01T09:05:00",
            description: "Drive 24 km to Horseshoe Bay Terminal",
        },
        {
            kind: "WAIT",
            start: "2026-01-01T09:05:00",
            end: "2026-01-01T09:50:00",
            description: "Arrive at Horseshoe Bay Terminal 15 minutes before booking check-in close",
        },
        {
            kind: "FERRY",
            start: "2026-01-01T09:50:00",
            end: "2026-01-01T10:30:00",
            description: "Ferry sailing from Horseshoe Bay Terminal to Langdale Terminal",
            from: "HSB",
            to: "LNG",
        },
        {
            kind: "DRIVE",
            start: "2026-01-01T10:30:00",
            end: "2026-01-01T11:47:00",
            description: "Drive 81 km to Earls Cove Terminal",
        },
        {
            kind: "FREE",
            start: "2026-01-01T11:47:00",
            end: "2026-01-01T12:35:00",
            description: "Free time",
        },
        {
            kind: "WAIT",
            start: "2026-01-01T12:35:00",
            end: "2026-01-01T12:55:00",
            description: "Arrive at Earls Cove Terminal 15 minutes before vehicles check-in close",
        },
        {
            kind: "FERRY",
            start: "2026-01-01T12:55:00",
            end: "2026-01-01T13:45:00",
            description: "Ferry sailing from Earls Cove Terminal to Saltery Bay Terminal",
            from: "ERL",
            to: "SLT",
        },
        {
            kind: "DRIVE",
            start: "2026-01-01T13:45:00",
            end: "2026-01-01T14:17:00",
            description: "Drive 35 km to Powell River",
        },
    ],
};
