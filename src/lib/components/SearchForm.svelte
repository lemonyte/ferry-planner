<script lang="ts">
    import { goto } from "$app/navigation";
    import { resolve } from "$app/paths";
    import { navigating } from "$app/state";
    import ArrowLeftRight from "@lucide/svelte/icons/arrow-left-right";
    import Check from "@lucide/svelte/icons/check";
    import LoaderCircle from "@lucide/svelte/icons/loader-circle";
    import RotateCcw from "@lucide/svelte/icons/rotate-ccw";
    import Search from "@lucide/svelte/icons/search";
    import SlidersHorizontal from "@lucide/svelte/icons/sliders-horizontal";
    import X from "@lucide/svelte/icons/x";

    import { CHECKINS, DEFAULT_EARLY, MAX_EARLY, type Query, toSearch } from "#lib/query.ts";

    import LocationPicker from "./LocationPicker.svelte";

    interface Props {
        query: Query;
    }

    let { query }: Props = $props();
    const id = $props.id();

    const CHECKIN_LABELS: Record<Query["checkin"], string> = {
        reservation: "Reservation",
        assured: "Assured loading",
        hostled: "Hostled vehicle",
    };

    let from = $derived(query.from);
    let to = $derived(query.to);
    let date = $derived(query.date);
    let checkin = $derived(query.checkin);
    let early = $derived(query.early);
    let long = $derived(query.long);

    const searching = $derived(navigating.to?.route.id === "/");
    const minutes = $derived(Math.min(Math.max(Math.round(early ?? DEFAULT_EARLY), 0), MAX_EARLY));
    const changes = $derived(Number(checkin !== "reservation") + Number(minutes !== DEFAULT_EARLY) + Number(long));

    let options: HTMLDialogElement;

    /** Go to the search URL, which omits options that are set to their defaults. */
    const search = () => {
        void goto(resolve("/") + toSearch({ ...query, from, to, date, checkin, early: minutes, long, all: false }));
    };

    /** Search again when the options dialog closes, if the options changed. */
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
    class="card p-3 sm:p-4 print:hidden"
    onsubmit={(event) => {
        event.preventDefault();
        if (options.open) {
            options.close();
        } else {
            search();
        }
    }}
>
    <div class="relative grid gap-2 sm:grid-cols-[1fr_auto_1fr] sm:items-end sm:gap-3">
        <LocationPicker name="from" label="From" bind:value={from} />
        <button
            type="button"
            class="btn-icon absolute top-1/2 right-3 z-1 -translate-y-1/2 border border-stone-300 bg-white text-stone-700 sm:static sm:mb-0.5 sm:translate-y-0"
            aria-label="Swap from and to"
            onclick={() => ([from, to] = [to, from])}
        >
            <ArrowLeftRight class="size-5 rotate-90 sm:rotate-0" />
        </button>
        <LocationPicker name="to" label="To" bind:value={to} />
    </div>
    <div
        class="mt-2 grid grid-cols-[minmax(0,1fr)_3rem_3rem] items-end gap-2 sm:mt-3 sm:grid-cols-[1fr_8rem_8rem] sm:gap-3"
    >
        <label class="block min-w-0">
            <span class="field-label">Date</span>
            <input
                type="date"
                required
                class="field block max-w-full min-w-0 appearance-none py-2.75 leading-6"
                bind:value={date}
            />
        </label>
        <button
            type="button"
            class="btn btn-secondary @container relative h-12 px-3"
            aria-haspopup="dialog"
            onclick={() => options.showModal()}
        >
            <SlidersHorizontal class="size-5 shrink-0" />
            <span class="label-if-fits">Options</span>
            {#if changes > 0}
                <span
                    class="absolute -top-2 -right-2 flex size-6 items-center justify-center rounded-full bg-amber-300 text-xs font-bold text-amber-950 ring-2 ring-white"
                >
                    {changes}
                    <span class="sr-only">{changes === 1 ? "change" : "changes"}</span>
                </span>
            {/if}
        </button>
        <button type="submit" class="btn btn-primary @container h-12 px-3 disabled:opacity-70" disabled={searching}>
            {#if searching}
                <LoaderCircle class="size-5 shrink-0 animate-spin" />
            {:else}
                <Search class="size-5 shrink-0" />
            {/if}
            <span class="label-if-fits">Search</span>
        </button>
    </div>
    <dialog
        bind:this={options}
        class="m-auto w-[calc(100%-2rem)] max-w-md rounded-xl bg-white text-stone-900 shadow-xl backdrop:bg-stone-900/50"
        aria-labelledby="{id}-options"
        closedby="any"
        onclose={applyOptions}
    >
        <div class="space-y-4 p-4">
            <div class="flex items-center justify-between">
                <h2 id="{id}-options" class="heading text-xl">Options</h2>
                <button
                    type="button"
                    class="btn-icon -m-2 text-stone-600"
                    aria-label="Close"
                    onclick={() => options.close()}
                >
                    <X class="size-5" />
                </button>
            </div>
            <fieldset>
                <legend class="mb-1 text-sm font-medium text-stone-700">Check-in</legend>
                {#each CHECKINS as kind (kind)}
                    <label class="flex min-h-11 items-center gap-3">
                        <input type="radio" class="size-5" name="checkin" value={kind} bind:group={checkin} />
                        {CHECKIN_LABELS[kind]}
                    </label>
                {/each}
            </fieldset>
            <label class="flex min-h-11 flex-wrap items-center gap-x-2">
                Arrive
                <input
                    type="number"
                    class="field h-11 w-20 px-2"
                    min="0"
                    max={MAX_EARLY}
                    inputmode="numeric"
                    bind:value={early}
                />
                minutes before check-in closes
            </label>
            <label class="flex min-h-11 items-center gap-3">
                <input type="checkbox" class="size-5" bind:checked={long} />
                Include long drives, overnight trips and later connections
            </label>
            <div class="flex justify-between gap-3">
                <button
                    type="button"
                    class="btn btn-secondary disabled:opacity-50"
                    disabled={changes === 0}
                    onclick={resetOptions}
                >
                    <RotateCcw class="size-4.5" />
                    Reset
                </button>
                <button type="button" class="btn btn-primary px-5" onclick={() => options.close()}>
                    <Check class="size-4.5" />
                    Done
                </button>
            </div>
        </div>
    </dialog>
</form>
