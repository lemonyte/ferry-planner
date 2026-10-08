<script lang="ts">
import ArrowLeft from "@lucide/svelte/icons/arrow-left";
import Check from "@lucide/svelte/icons/check";
import MapIcon from "@lucide/svelte/icons/map";
import Printer from "@lucide/svelte/icons/printer";
import Share from "@lucide/svelte/icons/share-2";
import TripSummary from "#lib/components/TripSummary.svelte";
import { formatDay, formatDuration, formatTime, secondsBetween } from "#lib/format.ts";
import { placeName } from "#lib/locations.ts";
import { toSearch } from "#lib/query.ts";
import type { Step } from "#lib/types.ts";
import { afterNavigate } from "$app/navigation";
import { resolve } from "$app/paths";

let { data } = $props();

const { query, itinerary } = $derived(data);

const DOTS: Record<Step["kind"], string> = {
    DRIVE: "bg-amber-400",
    WAIT: "bg-slate-300",
    FERRY: "bg-sky-700",
    FREE: "bg-emerald-300",
    MARK: "bg-slate-900",
};
// A button too narrow for its icon and what it says keeps the icon, and says the rest to those who cannot see it.
const BUTTON =
    "@container flex min-h-11 items-center justify-center gap-2 rounded-lg border border-slate-300 bg-white px-2 text-sm font-medium hover:bg-slate-100";
const LABEL = "sr-only @[5rem]:not-sr-only";

const journey = $derived(`${placeName(query.from)} to ${placeName(query.to)}`);

// Going back to the trips that this one was picked from leaves them as they were, scrolled to where they were.
let pickedFromTrips = $state(false);
afterNavigate(({ from }) => {
    pickedFromTrips = from?.route.id === "/";
});

let copied = $state(false);

const share = async () => {
    const shared = { title: document.title, url: window.location.href };
    if (navigator.canShare?.(shared)) {
        // Nothing is the matter when the share sheet is closed without sharing.
        await navigator.share(shared).catch(() => undefined);
    } else {
        await navigator.clipboard.writeText(shared.url);
        copied = true;
        setTimeout(() => {
            copied = false;
        }, 2000);
    }
};
</script>

<svelte:head>
    <title>{journey} · {formatTime(itinerary.depart)}, {formatDay(itinerary.depart)} · Ferry Planner</title>
    <meta name="description" content="A trip by BC Ferries, step by step.">
</svelte:head>

<a
    class="-ml-1 inline-flex min-h-11 items-center gap-1.5 font-medium text-sky-800 hover:text-sky-950 print:hidden"
    href={resolve("/") + toSearch(query)}
    onclick={(event) => {
        if (pickedFromTrips) {
            event.preventDefault();
            history.back();
        }
    }}
>
    <ArrowLeft class="size-5" />
    All trips
</a>

<div class="mt-2 flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1">
    <h1 class="text-xl font-bold">{journey}</h1>
    <p class="text-slate-600">{formatDay(itinerary.depart)}</p>
</div>

<div class="mt-3 rounded-xl border border-slate-200 bg-white p-4 print:border-0 print:p-0">
    <TripSummary {itinerary} />
    <ol class="mt-5 space-y-3 border-l-2 border-slate-200 pl-4">
        {#each itinerary.steps as step, index (index)}
            {@const seconds = secondsBetween(step.start, step.end)}
            <li class="relative">
                <span
                    class={[
                        "absolute top-1.5 -left-[1.4rem] size-2.5 rounded-full ring-2 ring-white",
                        DOTS[step.kind],
                    ]}
                ></span>
                <div class="flex flex-wrap items-baseline gap-x-2">
                    <time class="w-18 shrink-0 text-sm text-slate-600 tabular-nums" datetime={step.start}
                        >{formatTime(step.start)}</time
                    >
                    <span class={["min-w-0 flex-1 basis-48", step.kind === "MARK" && "font-semibold"]}>
                        {step.description}
                        {#if seconds > 0}
                            <span class="text-sm whitespace-nowrap text-slate-500">· {formatDuration(seconds)}</span>
                        {/if}
                    </span>
                </div>
                {#if step.scheduleUrl}
                    <a
                        class="ml-20 inline-flex min-h-8 items-center text-sm text-sky-800 underline print:hidden"
                        href={step.scheduleUrl}
                        target="_blank"
                        rel="noopener"
                    >
                        BC Ferries schedule
                    </a>
                {/if}
            </li>
        {/each}
    </ol>
</div>

<div class="mt-4 grid max-w-md grid-cols-3 gap-2 print:hidden">
    <a class={BUTTON} href={itinerary.mapUrl} target="_blank" rel="noopener">
        <MapIcon class="size-4.5 shrink-0" />
        <span class={LABEL}>Map</span>
    </a>
    <button type="button" class={BUTTON} onclick={share}>
        {#if copied}
            <Check class="size-4.5 shrink-0" />
        {:else}
            <Share class="size-4.5 shrink-0" />
        {/if}
        <span class={LABEL}>{copied ? "Copied" : "Share"}</span>
    </button>
    <button type="button" class={BUTTON} onclick={() => window.print()}>
        <Printer class="size-4.5 shrink-0" />
        <span class={LABEL}>Print</span>
    </button>
</div>
