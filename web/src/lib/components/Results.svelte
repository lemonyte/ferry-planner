<script lang="ts">
import Car from "@lucide/svelte/icons/car";
import Clock from "@lucide/svelte/icons/clock";
import Coffee from "@lucide/svelte/icons/coffee";
import Layers from "@lucide/svelte/icons/layers";
import Ship from "@lucide/svelte/icons/ship";
import { addDays, formatDay, formatDistance } from "#lib/format.ts";
import { placeName, shortName } from "#lib/locations.ts";
import { type Query, SORTS, toSearch } from "#lib/query.ts";
import { sortItineraries } from "#lib/sort.ts";
import type { Itinerary, SearchResult } from "#lib/types.ts";
import { resolve } from "$app/paths";
import TripSummary from "./TripSummary.svelte";

interface Props {
    query: Query;
    result: SearchResult;
}

let { query, result }: Props = $props();

const TOMORROW = $derived({ date: addDays(query.date, 1), all: false, underway: false });

const LEGEND = [
    [Car, "bg-amber-300 text-amber-950", "Drive"],
    [Clock, "bg-slate-200 text-slate-700", "Check-in"],
    [Ship, "bg-sky-700 text-white", "Ferry"],
    [Coffee, "bg-emerald-200 text-emerald-950", "Free time"],
] as const;
/** Number of trips of a route shown before the rest are asked for. */
const SHOWN = 5;
const BUTTON = "inline-flex min-h-11 items-center rounded-lg px-4 font-semibold";
const NOTE_LINK = "inline-flex min-h-8 items-center font-medium text-sky-800 underline";
// On a phone, the trips go from one side of the screen to the other, for their bars to be as wide as can be.
const BLEED = "-mx-4 border-x-0 sm:mx-0 sm:rounded-xl sm:border-x";
const CHOICE = "flex min-h-10 items-center rounded-md px-3 text-sm font-medium";
const CHOSEN = "bg-sky-700 text-white";
// Showing the trips another way leaves the page where it is, and going back does not go through each way shown.
const STAY = { "data-sveltekit-replacestate": true, "data-sveltekit-reset": "false" } as const;
const SORT_LABELS: Record<Query["sort"], string> = {
    duration: "Duration",
    departure: "Departure",
    arrival: "Arrival",
};

const journey = $derived(`${placeName(query.from)} to ${placeName(query.to)}`);
const itineraries = $derived(sortItineraries(result.itineraries, query.sort));
const longest = $derived(Math.max(...itineraries.map((itinerary) => itinerary.duration)));
// Only one trip is marked as the fastest, and none when there is nothing to compare it to.
const fastest = $derived(itineraries.length > 1 ? sortItineraries(itineraries, "duration")[0] : undefined);
// The trips of each route, the route with the first of the trips first.
const routes = $derived.by(() => {
    const routes = new Map<string, Itinerary[]>();
    for (const itinerary of itineraries) {
        routes.set(itinerary.route, [...(routes.get(itinerary.route) ?? []), itinerary]);
    }
    return [...routes.values()];
});

/** Link to the same search shown another way, which is searched again as other routes can then be the best. */
const linkTo = (change: Partial<Query>): string => {
    return resolve("/") + toSearch({ ...query, ...change });
};

const sailingsOf = (itinerary: Itinerary): string[] => {
    return itinerary.steps.flatMap((step) =>
        step.from && step.to ? [`${shortName(step.from)} → ${shortName(step.to)}`] : [],
    );
};
</script>

{#snippet trip(
    itinerary: Itinerary,
)}
    <a
        class="block p-4 hover:bg-slate-50 focus-visible:bg-slate-50"
        href={resolve("/trip/[id]", { id: itinerary.id }) + toSearch(query)}
    >
        <TripSummary
            {itinerary}
            {longest}
            fastest={itinerary === fastest}
            left={itinerary.depart < result.now}
            sailings={!query.group}
        />
    </a>
{/snippet}

<div class="mt-6 flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1">
    <h1 class="text-xl font-bold">{journey}</h1>
    <p class="text-slate-600">{formatDay(query.date)}</p>
</div>

{#if result.itineraries.length === 0}
    <div class="mt-4 rounded-xl border border-slate-200 bg-white p-4">
        {#if result.departed > 0}
            <p>Every way to get there on this day has already left.</p>
            <div class="mt-3 flex flex-wrap gap-2">
                <a class={[BUTTON, "bg-sky-700 text-white hover:bg-sky-800"]} href={linkTo(TOMORROW)}>
                    See {formatDay(addDays(query.date, 1))}
                </a>
                {#if result.underway > 0}
                    <a
                        class={[BUTTON, "border border-slate-300 hover:bg-slate-100"]}
                        href={linkTo({ underway: true })}
                    >
                        Show trips under way
                    </a>
                {/if}
            </div>
        {:else if !result.covered}
            <p>BC Ferries has not posted its schedules for this date yet.</p>
        {:else}
            <p>There is no way to get there on this day. Try another date, or include long drives in the options.</p>
        {/if}
    </div>
{:else}
    {#if !result.covered}
        <p class="mt-3 text-sm text-slate-600">
            BC Ferries has not posted its schedules for this date yet, so only trips without a ferry are shown.
        </p>
    {:else if query.underway}
        <p class="mt-3 text-sm text-slate-600">
            Trips that have left but not arrived yet are shown.
            <a class={NOTE_LINK} href={linkTo({ underway: false })} {...STAY}>Hide them</a>
        </p>
    {:else if result.departed > 0}
        <p class="mt-3 text-sm text-slate-600">
            Trips that have already left today are not shown.
            {#if result.underway > 0}
                <a class={NOTE_LINK} href={linkTo({ underway: true })} {...STAY}>Show those still under way</a>
            {/if}
        </p>
    {/if}
    <ul class="mt-3 flex flex-wrap gap-x-4 gap-y-1 text-sm text-slate-600" aria-label="Colours of the bars">
        {#each LEGEND as [Icon, color, label] (label)}
            <li class="flex items-center gap-1.5">
                <span class={["flex size-5 items-center justify-center rounded", color]}>
                    <Icon class="size-3.5" />
                </span>
                {label}
            </li>
        {/each}
    </ul>
    <div class="mt-3 flex flex-wrap items-center justify-end gap-x-4 gap-y-2 sm:justify-start print:hidden">
        <nav class="flex flex-wrap items-center justify-end gap-2" aria-label="Sort by">
            <span class="text-sm whitespace-nowrap text-slate-600" aria-hidden="true">Sort by</span>
            <div class="flex rounded-lg border border-slate-300 bg-white p-0.5">
                {#each SORTS as sort (sort)}
                    <a
                        class={[CHOICE, sort === query.sort ? CHOSEN : "text-slate-700 hover:bg-slate-100"]}
                        href={linkTo({ sort })}
                        aria-current={sort === query.sort}
                        {...STAY}
                    >
                        {SORT_LABELS[sort]}
                    </a>
                {/each}
            </div>
        </nav>
        <a
            class={[
                CHOICE,
                "gap-2 border",
                query.group
                    ? [CHOSEN, "border-sky-700"]
                    : "border-slate-300 bg-white text-slate-700 hover:bg-slate-100",
            ]}
            href={linkTo({ group: !query.group })}
            role="switch"
            aria-checked={query.group}
            {...STAY}
        >
            <Layers class="size-4" />
            Group by route
        </a>
    </div>
    {#if query.group}
        <div class="mt-3 space-y-4">
            {#each routes as trips (trips[0]?.route)}
                {@const [first] = trips}
                {@const sailings = first ? sailingsOf(first) : []}
                <section class={["border border-slate-200 bg-white", BLEED]}>
                    <header class="px-4 pt-4 pb-3">
                        <h2 class="text-lg leading-snug font-semibold">
                            {#each sailings as sailing, index (index)}
                                <span class="block">{sailing}</span>
                            {:else}
                                No ferry
                            {/each}
                        </h2>
                        <p class="mt-1 text-sm text-slate-600">
                            {trips.length} {trips.length === 1 ? "trip" : "trips"}
                            {#if first && first.drivingDistance > 0}
                                · {formatDistance(first.drivingDistance)} driving
                            {/if}
                        </p>
                    </header>
                    <ol class="divide-y divide-slate-200 border-t border-slate-200">
                        {#each trips.slice(0, SHOWN) as itinerary (itinerary.id)}
                            <li>{@render trip(itinerary)}</li>
                        {/each}
                    </ol>
                    {#if trips.length > SHOWN}
                        <details class="border-t border-slate-200">
                            <summary
                                class="flex min-h-11 cursor-pointer items-center px-4 text-sm font-medium text-sky-800"
                            >
                                Show {trips.length - SHOWN} more
                            </summary>
                            <ol class="divide-y divide-slate-200 border-t border-slate-200">
                                {#each trips.slice(SHOWN) as itinerary (itinerary.id)}
                                    <li>{@render trip(itinerary)}</li>
                                {/each}
                            </ol>
                        </details>
                    {/if}
                </section>
            {/each}
        </div>
    {:else}
        <ol class={["mt-3 divide-y divide-slate-200 border border-slate-200 bg-white", BLEED]}>
            {#each itineraries as itinerary (itinerary.id)}
                <li>{@render trip(itinerary)}</li>
            {/each}
        </ol>
    {/if}
    {#if result.moreRoutes > 0}
        <a
            class="mt-4 flex min-h-11 items-center justify-center rounded-lg border border-slate-300 bg-white px-4 font-medium text-sky-800 hover:bg-slate-100 print:hidden"
            href={linkTo({ all: true })}
            data-sveltekit-reset="false"
        >
            Show {result.moreRoutes} more {result.moreRoutes === 1 ? "route" : "routes"}
        </a>
    {/if}
{/if}
