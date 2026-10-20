<script lang="ts">
    import { afterNavigate } from "$app/navigation";
    import { resolve } from "$app/paths";
    import ArrowLeft from "@lucide/svelte/icons/arrow-left";
    import Check from "@lucide/svelte/icons/check";
    import MapIcon from "@lucide/svelte/icons/map";
    import Printer from "@lucide/svelte/icons/printer";
    import Share from "@lucide/svelte/icons/share-2";

    import Head from "#lib/components/Head.svelte";
    import Notices from "#lib/components/Notices.svelte";
    import TripSummary from "#lib/components/TripSummary.svelte";
    import { formatDay, formatDuration, formatTime, secondsBetween } from "#lib/format.ts";
    import { placeName } from "#lib/locations.ts";
    import { toSearch } from "#lib/query.ts";
    import { SITE_NAME } from "#lib/site.ts";
    import { sailingNames, STEP_KINDS } from "#lib/steps.ts";

    let { data } = $props();

    const { query, itinerary } = $derived(data);

    const journey = $derived(`${placeName(query.from)} to ${placeName(query.to)}`);
    const sailings = $derived(sailingNames(itinerary));

    // Going back to the trip list that this trip was opened from keeps its state and scroll position.
    let pickedFromTrips = $state(false);
    afterNavigate(({ from }) => {
        pickedFromTrips = from?.route.id === "/";
    });

    let copied = $state(false);
    let copiedTimer: ReturnType<typeof setTimeout> | undefined;

    const share = async () => {
        const shared = { title: document.title, url: window.location.href };
        if (navigator.canShare?.(shared)) {
            // Closing the share sheet without sharing rejects, which is not an error.
            await navigator.share(shared).catch(() => undefined);
        } else {
            try {
                await navigator.clipboard.writeText(shared.url);
            } catch (error) {
                // Copying can be blocked. The link is still in the address bar.
                console.warn("failed to copy the link", error);
                return;
            }
            copied = true;
            clearTimeout(copiedTimer);
            copiedTimer = setTimeout(() => {
                copied = false;
            }, 2000);
        }
    };
</script>

<Head
    title="{journey} · {formatTime(itinerary.depart)}, {formatDay(itinerary.depart)} · {SITE_NAME}"
    description="Leave at {formatTime(itinerary.depart)} and arrive at {formatTime(itinerary.arrive)} on {formatDay(
        itinerary.depart,
    )}, {formatDuration(itinerary.duration)} in all{sailings.length > 0 ? `, by ${sailings.join(' and ')}` : ''}."
/>

<a
    class="-ml-1 inline-flex min-h-11 items-center gap-1.5 font-medium text-sea-800 hover:text-sea-950 print:hidden"
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

<div class="title-row mt-2">
    <h1 class="heading text-2xl">{journey}</h1>
    <p class="text-stone-600">{formatDay(itinerary.depart)}</p>
</div>

<div class="mt-4 grid max-w-md grid-cols-3 gap-2 print:hidden">
    <a class="btn btn-secondary @container px-2 text-sm" href={itinerary.mapUrl} target="_blank" rel="noopener">
        <MapIcon class="size-4.5 shrink-0" />
        <span class="label-if-fits">Map</span>
    </a>
    <button type="button" class="btn btn-secondary @container px-2 text-sm" onclick={share}>
        {#if copied}
            <Check class="size-4.5 shrink-0" />
        {:else}
            <Share class="size-4.5 shrink-0" />
        {/if}
        <span class="label-if-fits">{copied ? "Copied" : "Share"}</span>
    </button>
    <button type="button" class="btn btn-secondary @container px-2 text-sm" onclick={() => window.print()}>
        <Printer class="size-4.5 shrink-0" />
        <span class="label-if-fits">Print</span>
    </button>
</div>

<div class="card-bleed mt-3 p-4 print:border-0 print:p-0">
    <TripSummary {itinerary} />
    <ol class="mt-5 space-y-3 border-l-2 border-stone-200 pl-4">
        {#each itinerary.steps as step}
            {@const seconds = secondsBetween(step.start, step.end)}
            <li class="relative">
                <span class={["step-dot", step.kind === "MARK" ? "bg-stone-900" : STEP_KINDS[step.kind].dot]}></span>
                <div class="flex flex-wrap items-baseline gap-x-2">
                    <time class="w-18 shrink-0 text-sm text-stone-600 tabular-nums" datetime={step.start}
                        >{formatTime(step.start)}</time
                    >
                    <span class={["min-w-0 flex-1 basis-48", step.kind === "MARK" && "font-semibold"]}>
                        {step.description}
                        {#if seconds > 0}
                            <span class="text-sm whitespace-nowrap text-stone-500">· {formatDuration(seconds)}</span>
                        {/if}
                    </span>
                </div>
                {#if step.scheduleUrl}
                    <a class="link ml-20 text-sm print:hidden" href={step.scheduleUrl} target="_blank" rel="noopener">
                        BC Ferries schedule
                    </a>
                {/if}
            </li>
        {/each}
    </ol>
</div>

<Notices />
