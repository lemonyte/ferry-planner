import Car from "@lucide/svelte/icons/car";
import Clock from "@lucide/svelte/icons/clock";
import Coffee from "@lucide/svelte/icons/coffee";
import Ship from "@lucide/svelte/icons/ship";

import { shortName } from "./locations.ts";
import type { Itinerary, Step } from "./planner/itinerary.ts";

/** Icon, label, and Tailwind classes for each kind of step that has a duration. */
export const STEP_KINDS = {
    DRIVE: { icon: Car, label: "Drive", bar: "bg-amber-300 text-amber-950", dot: "bg-amber-400" },
    WAIT: { icon: Clock, label: "Check-in", bar: "bg-slate-200 text-slate-700", dot: "bg-slate-300" },
    FERRY: { icon: Ship, label: "Ferry", bar: "bg-sky-700 text-white", dot: "bg-sky-700" },
    FREE: { icon: Coffee, label: "Free time", bar: "bg-emerald-200 text-emerald-950", dot: "bg-emerald-300" },
} as const satisfies Record<Exclude<Step["kind"], "MARK">, object>;

/** Name a sailing step by its terminals. Returns `undefined` for other steps. */
export const sailingName = (step: Step): string | undefined => {
    return step.from && step.to ? `${shortName(step.from)} → ${shortName(step.to)}` : undefined;
};

/** Name the sailings of a trip, in order. */
export const sailingNames = (itinerary: Itinerary): string[] => {
    return itinerary.steps.flatMap((step) => sailingName(step) ?? []);
};
