<script lang="ts">
import ArrowLeftRight from "@lucide/svelte/icons/arrow-left-right";
import Check from "@lucide/svelte/icons/check";
import LoaderCircle from "@lucide/svelte/icons/loader-circle";
import RotateCcw from "@lucide/svelte/icons/rotate-ccw";
import Search from "@lucide/svelte/icons/search";
import SlidersHorizontal from "@lucide/svelte/icons/sliders-horizontal";
import X from "@lucide/svelte/icons/x";
import { CHECKINS, DEFAULT_EARLY, MAX_EARLY, type Query, toSearch } from "#lib/query.ts";
import { goto } from "$app/navigation";
import { resolve } from "$app/paths";
import { navigating } from "$app/state";
import LocationPicker from "./LocationPicker.svelte";

interface Props {
    query: Query;
}

let { query }: Props = $props();
const id = $props.id();

// A button too narrow for its icon and what it says keeps the icon, and says the rest to those who cannot see it.
const LABEL = "sr-only @[6rem]:not-sr-only";

// On a phone, what a field is for is only said to those who cannot see where it is.
const FIELD_LABEL = "sr-only text-sm font-medium text-slate-700 sm:not-sr-only sm:mb-1 sm:block";

const CHECKIN_LABELS: Record<Query["checkin"], string> = {
    reservation: "Reservation",
    assured: "Assured loading",
    hostled: "Hostled vehicle",
};

// What is picked in the form, starting from the search that the page shows.
let from = $derived(query.from);
let to = $derived(query.to);
let date = $derived(query.date);
let checkin = $derived(query.checkin);
let early = $derived(query.early);
let long = $derived(query.long);

const searching = $derived(navigating.to !== null);
// Minutes to arrive early as they are searched with, whatever is typed.
const minutes = $derived(Math.min(Math.max(Math.round(early ?? DEFAULT_EARLY), 0), MAX_EARLY));
const changes = $derived(Number(checkin !== "reservation") + Number(minutes !== DEFAULT_EARLY) + Number(long));

let options: HTMLDialogElement;

const swap = () => {
    [from, to] = [to, from];
};

/** Go to the search by a link that leaves out the options that are as usual, which submitting the form would not. */
const search = () => {
    goto(resolve("/") + toSearch({ ...query, from, to, date, checkin, early: minutes, long, all: false }));
};

/** Search again once the options are closed, if they are no longer those that the search shown was made with. */
const applyOptions = () => {
    const changed = checkin !== query.checkin || minutes !== query.early || long !== query.long;
    if (changed && query.from && query.to && from && to) {
        search();
    }
};

const resetOptions = () => {
    checkin = "reservation";
    early = DEFAULT_EARLY;
    long = false;
};
</script>

<form
    method="GET"
    action={resolve("/")}
    class="rounded-xl border border-slate-200 bg-white p-3 sm:p-4 print:hidden"
    onsubmit={(event) => {
        event.preventDefault();
        // Submitted from the options, the form closes them, which searches if they have changed.
        if (options.open) {
            options.close();
        } else {
            search();
        }
    }}
>
    <!-- On a phone, the button to swap sits over the gap between the two places, to save the height of a row. -->
    <div class="relative grid gap-2 sm:grid-cols-[1fr_auto_1fr] sm:items-end sm:gap-3">
        <LocationPicker name="from" label="From" bind:value={from} />
        <button
            type="button"
            class="absolute top-1/2 right-3 z-1 flex size-11 -translate-y-1/2 items-center justify-center rounded-full border border-slate-300 bg-white text-slate-700 hover:bg-slate-100 sm:static sm:mb-0.5 sm:translate-y-0"
            aria-label="Swap from and to"
            onclick={swap}
        >
            <ArrowLeftRight class="size-5 rotate-90 sm:rotate-0" />
        </button>
        <LocationPicker name="to" label="To" bind:value={to} />
    </div>
    <!-- On a phone, the date and the buttons share a row, and the buttons are only their icons. -->
    <div
        class="mt-2 grid grid-cols-[minmax(0,1fr)_3rem_3rem] items-end gap-2 sm:mt-3 sm:grid-cols-[1fr_8rem_8rem] sm:gap-3"
    >
        <label class="block min-w-0">
            <span class={FIELD_LABEL}>Date</span>
            <input
                type="date"
                name="date"
                required
                class="block h-12 w-full max-w-full min-w-0 appearance-none rounded-lg border border-slate-300 bg-white px-3 py-[calc(0.75rem-1px)] text-base leading-6"
                bind:value={date}
            >
        </label>
        <button
            type="button"
            class="@container relative flex h-12 items-center justify-center gap-2 rounded-lg border border-slate-300 bg-white px-3 text-base font-medium hover:bg-slate-100"
            aria-haspopup="dialog"
            onclick={() => options.showModal()}
        >
            <SlidersHorizontal class="size-5 shrink-0" />
            <span class={LABEL}>Options</span>
            {#if changes > 0}
                <span
                    class="absolute -top-2 -right-2 flex size-6 items-center justify-center rounded-full bg-amber-300 text-xs font-bold text-amber-950 ring-2 ring-white"
                >
                    {changes}
                    <span class="sr-only">{changes === 1 ? "change" : "changes"}</span>
                </span>
            {/if}
        </button>
        <button
            type="submit"
            class="@container flex h-12 items-center justify-center gap-2 rounded-lg bg-sky-700 px-3 text-base font-semibold text-white hover:bg-sky-800 disabled:opacity-70"
            disabled={searching}
        >
            {#if searching}
                <LoaderCircle class="size-5 shrink-0 animate-spin" />
            {:else}
                <Search class="size-5 shrink-0" />
            {/if}
            <span class={LABEL}>Search</span>
        </button>
    </div>
    <dialog
        bind:this={options}
        class="m-auto w-[calc(100%-2rem)] max-w-md rounded-xl bg-white text-slate-900 shadow-xl backdrop:bg-slate-900/50"
        aria-labelledby="{id}-options"
        closedby="any"
        onclose={applyOptions}
    >
        <div class="space-y-4 p-4">
            <div class="flex items-center justify-between">
                <h2 id="{id}-options" class="text-lg font-bold">Options</h2>
                <button
                    type="button"
                    class="-m-2 flex size-11 items-center justify-center rounded-full text-slate-600 hover:bg-slate-100"
                    aria-label="Close"
                    onclick={() => options.close()}
                >
                    <X class="size-5" />
                </button>
            </div>
            <fieldset>
                <legend class="mb-1 text-sm font-medium text-slate-700">Check-in</legend>
                {#each CHECKINS as kind (kind)}
                    <label class="flex min-h-11 items-center gap-3">
                        <input type="radio" class="size-5" name="checkin" value={kind} bind:group={checkin}>
                        {CHECKIN_LABELS[kind]}
                    </label>
                {/each}
            </fieldset>
            <label class="flex min-h-11 flex-wrap items-center gap-x-2">
                Arrive
                <input
                    type="number"
                    class="h-11 w-20 rounded-lg border border-slate-300 bg-white px-2 text-base"
                    name="early"
                    min="0"
                    max={MAX_EARLY}
                    inputmode="numeric"
                    bind:value={early}
                >
                minutes before check-in closes
            </label>
            <label class="flex min-h-11 items-center gap-3">
                <input type="checkbox" class="size-5" name="long" value="1" bind:checked={long}>
                Include long drives, overnight trips and later connections
            </label>
            <div class="flex justify-between gap-3">
                <button
                    type="button"
                    class="flex h-11 items-center gap-2 rounded-lg border border-slate-300 px-4 font-medium hover:bg-slate-100 disabled:opacity-50"
                    disabled={changes === 0}
                    onclick={resetOptions}
                >
                    <RotateCcw class="size-4.5" />
                    Reset
                </button>
                <button
                    type="button"
                    class="flex h-11 items-center gap-2 rounded-lg bg-sky-700 px-5 font-semibold text-white hover:bg-sky-800"
                    onclick={() => options.close()}
                >
                    <Check class="size-4.5" />
                    Done
                </button>
            </div>
        </div>
    </dialog>
</form>
