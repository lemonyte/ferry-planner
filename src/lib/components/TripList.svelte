<script lang="ts">
    import { goto } from "$app/navigation";
    import { resolve } from "$app/paths";
    import Layers from "@lucide/svelte/icons/layers";

    import { addDays, formatDay, formatDistance } from "#lib/format.ts";
    import { placeName } from "#lib/locations.ts";
    import type { Itinerary, SearchResult } from "#lib/planner/itinerary.ts";
    import { type Query, SORTS, toSearch } from "#lib/query.ts";
    import { compareItineraries } from "#lib/sort.ts";
    import { sailingNames } from "#lib/steps.ts";

    import Legend from "./Legend.svelte";
    import Notices from "./Notices.svelte";
    import TripSummary from "./TripSummary.svelte";

    interface Props {
        query: Query;
        result: SearchResult;
    }

    let { query, result }: Props = $props();

    const tomorrow = $derived(addDays(query.date, 1));

    /** Number of trips shown per route before the rest are expanded. */
    const TRIPS_PER_ROUTE_GROUP = 3;
    // Sort and filter links replace the history entry and keep the scroll position.
    const STAY = { "data-sveltekit-replacestate": true, "data-sveltekit-reset": "false" } as const;
    const SORT_LABELS: Record<Query["sort"], string> = {
        duration: "Duration",
        departure: "Departure",
        arrival: "Arrival",
    };

    const journey = $derived(`${placeName(query.from)} to ${placeName(query.to)}`);
    // Already sorted by `query.sort`.
    const { itineraries } = $derived(result);
    const longest = $derived(Math.max(...itineraries.map((itinerary) => itinerary.duration)));
    // Marks a single trip as the fastest, and none if only one trip is shown.
    const fastest = $derived(itineraries.length > 1 ? itineraries.toSorted(compareItineraries.duration)[0] : undefined);
    // Trips grouped by route, in order of the first trip of each route.
    const routes = $derived([...Map.groupBy(itineraries, (itinerary) => itinerary.route).values()]);

    /** Link to the same search with some options changed. */
    const linkTo = (change: Partial<Query>): string => {
        return resolve("/") + toSearch({ ...query, ...change });
    };
</script>

{#snippet trip(itinerary: Itinerary)}
    <a
        class="block p-4 hover:bg-stone-50 focus-visible:bg-stone-50"
        href={resolve("/trip/[id]", { id: itinerary.id }) + toSearch(query)}
    >
        <TripSummary {itinerary} {longest} fastest={itinerary === fastest} left={itinerary.depart < result.now} />
    </a>
{/snippet}

<div class="title-row mt-6">
    <h1 class="heading text-2xl">{journey}</h1>
    <p class="text-stone-600">{formatDay(query.date)}</p>
</div>

{#if result.itineraries.length === 0}
    <div class="card mt-4 p-4">
        {#if result.departed > 0}
            <p>Every way to get there on this day has already left.</p>
            <div class="mt-3 flex flex-wrap gap-2">
                <a class="btn btn-primary" href={linkTo({ date: tomorrow, all: false, underway: false })}>
                    See {formatDay(tomorrow)}
                </a>
                {#if result.underway > 0}
                    <a class="btn btn-secondary" href={linkTo({ underway: true })}>Show trips under way</a>
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
        <p class="mt-3 text-sm text-stone-600">
            BC Ferries has not posted its schedules for this date yet, so only trips without a ferry are shown.
        </p>
    {:else if query.underway}
        <p class="mt-3 text-sm text-stone-600">
            Trips that have left but not arrived yet are shown.
            <a class="link font-medium" href={linkTo({ underway: false })} {...STAY}>Hide them</a>
        </p>
    {:else if result.departed > 0}
        <p class="mt-3 text-sm text-stone-600">
            Trips that have already left today are not shown.
            {#if result.underway > 0}
                <a class="link font-medium" href={linkTo({ underway: true })} {...STAY}>Show those still under way</a>
            {/if}
        </p>
    {/if}
    <div class="mt-3"><Legend /></div>
    <div class="mt-3 flex flex-wrap items-center justify-end gap-x-4 gap-y-2 sm:justify-start print:hidden">
        <nav class="flex flex-wrap items-center justify-end gap-2" aria-label="Sort by">
            <span class="text-sm whitespace-nowrap text-stone-600" aria-hidden="true">Sort by</span>
            <div class="flex rounded-lg border border-stone-300 bg-white p-0.5">
                {#each SORTS as sort (sort)}
                    <a class="choice" href={linkTo({ sort })} aria-current={sort === query.sort} {...STAY}>
                        {SORT_LABELS[sort]}
                    </a>
                {/each}
            </div>
        </nav>
        <button
            type="button"
            class="choice border border-stone-300 bg-white aria-checked:border-sea-700"
            role="switch"
            aria-checked={query.group}
            onclick={() => void goto(linkTo({ group: !query.group }), { replace: true, reset: false })}
        >
            <Layers class="size-4" />
            Group by route
        </button>
    </div>
    {#if query.group}
        <div class="mt-3 space-y-4">
            {#each routes as trips (trips[0]?.route)}
                {@const [first] = trips}
                {@const sailings = first ? sailingNames(first) : []}
                <section class="card-bleed">
                    <header class="px-4 pt-4 pb-3">
                        <h2 class="font-display text-xl leading-tight font-semibold">
                            {#each sailings as sailing}
                                <span class="block">{sailing}</span>
                            {:else}
                                No ferry
                            {/each}
                        </h2>
                        <p class="mt-1 text-sm text-stone-600">
                            {trips.length}
                            {trips.length === 1 ? "trip" : "trips"}
                            {#if first && first.drivingDistance > 0}
                                · {formatDistance(first.drivingDistance)} driving
                            {/if}
                        </p>
                    </header>
                    <ol class="divide-y divide-stone-200 border-t border-stone-200">
                        {#each trips.slice(0, TRIPS_PER_ROUTE_GROUP) as itinerary (itinerary.id)}
                            <li>{@render trip(itinerary)}</li>
                        {/each}
                    </ol>
                    {#if trips.length > TRIPS_PER_ROUTE_GROUP}
                        <details class="group border-t border-stone-200">
                            <summary
                                class="flex min-h-11 select-none items-center px-4 text-sm font-medium text-sea-800"
                            >
                                <span>
                                    <span class="group-open:hidden">Show</span><span class="hidden group-open:inline"
                                        >Hide</span
                                    >
                                    {trips.length - TRIPS_PER_ROUTE_GROUP} more
                                </span>
                            </summary>
                            <ol class="divide-y divide-stone-200 border-t border-stone-200">
                                {#each trips.slice(TRIPS_PER_ROUTE_GROUP) as itinerary (itinerary.id)}
                                    <li>{@render trip(itinerary)}</li>
                                {/each}
                            </ol>
                        </details>
                    {/if}
                </section>
            {/each}
        </div>
    {:else}
        <ol class="card-bleed mt-3 divide-y divide-stone-200">
            {#each itineraries as itinerary (itinerary.id)}
                <li>{@render trip(itinerary)}</li>
            {/each}
        </ol>
    {/if}
    {#if result.more > 0}
        <a
            class="btn btn-secondary mt-4 flex text-sea-800 print:hidden"
            href={linkTo({ all: true })}
            data-sveltekit-reset="false"
        >
            Show {result.more} more {result.more === 1 ? "trip" : "trips"}
        </a>
    {/if}
    <Notices />
{/if}
