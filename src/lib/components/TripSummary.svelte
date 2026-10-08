<script lang="ts">
import Car from "@lucide/svelte/icons/car";
import Clock from "@lucide/svelte/icons/clock";
import Coffee from "@lucide/svelte/icons/coffee";
import Ship from "@lucide/svelte/icons/ship";
import { daysBetween, formatDistance, formatDuration, formatTime, secondsBetween } from "#lib/format.ts";
import { shortName } from "#lib/locations.ts";
import type { Itinerary, Step } from "#lib/types.ts";

interface Props {
    itinerary: Itinerary;
    /** Duration in seconds of the longest trip shown, which the bars are in proportion to. */
    longest?: number;
    /** Whether no other trip shown is faster. */
    fastest?: boolean;
    /** Whether the trip has already left. */
    left?: boolean;
    /** Whether to say which sailings the trip is by, where that is not said for all of its route already. */
    sailings?: boolean;
}

let {
    itinerary,
    longest = itinerary.duration,
    fastest = false,
    left = false,
    sailings: showSailings = true,
}: Props = $props();

const KINDS = {
    DRIVE: { icon: Car, color: "bg-amber-300 text-amber-950" },
    WAIT: { icon: Clock, color: "bg-slate-200 text-slate-700" },
    FERRY: { icon: Ship, color: "bg-sky-700 text-white" },
    FREE: { icon: Coffee, color: "bg-emerald-200 text-emerald-950" },
} as const;

// Widths of a letter in ems, taken wide enough that what is said to fit does.
const BOLD = 0.68;
const PLAIN = 0.58;

interface Part {
    step: Step;
    kind: keyof typeof KINDS;
    seconds: number;
    /** Widths in ems of what the part can say: the least, that and how long it takes, and its terminals by name. */
    widths: { text: number; both?: number; names?: number };
}

const toWidths = (step: Step, seconds: number): Part["widths"] => {
    const time = formatDuration(seconds).length * PLAIN;
    if (!step.from || !step.to) {
        return { text: time };
    }
    const codes = `${step.from} → ${step.to}`.length * BOLD;
    const names = `${shortName(step.from)} → ${shortName(step.to)}`.length * BOLD;
    // The names go beside the icon, which is a letter and a half wide with the gap after it.
    return { text: codes, both: codes + 3 * PLAIN + time, names: Math.max(names + 1.75, time) };
};

const parts = $derived(
    itinerary.steps.flatMap((step): Part[] => {
        const seconds = secondsBetween(step.start, step.end);
        return step.kind !== "MARK" && seconds > 0
            ? [{ step, kind: step.kind, seconds, widths: toWidths(step, seconds) }]
            : [];
    }),
);
const sailings = $derived(
    itinerary.steps.flatMap((step) =>
        step.from && step.to ? [`${shortName(step.from)} → ${shortName(step.to)}`] : [],
    ),
);
const laterDays = $derived(daysBetween(itinerary.depart, itinerary.arrive));

/** Part of the bar that the pointer is over, and where its details go, in pixels from the left of the bar. */
let tip = $state<{ part: Part; center: number; min: number; max: number }>();
let tipWidth = $state(0);

const showTip = (event: PointerEvent & { currentTarget: HTMLElement }) => {
    const element = event.target instanceof Element ? event.target.closest<HTMLElement>("[data-part]") : null;
    const part = parts[Number(element?.dataset.part)];
    // Touching a part goes to the trip, which has the details.
    if (!element || !part || event.pointerType !== "mouse") {
        tip = undefined;
        return;
    }
    const bar = event.currentTarget.getBoundingClientRect();
    const box = element.getBoundingClientRect();
    tip = {
        part,
        center: box.left + box.width / 2 - bar.left,
        // The details stay within the page, however close to its side the part is.
        min: 8 - bar.left,
        max: document.documentElement.clientWidth - 8 - bar.left,
    };
};
</script>

<!-- Above the bar and not within its width, as the bar of a short trip is narrower than this. -->
<p class="flex flex-wrap items-center gap-x-2 gap-y-1 whitespace-nowrap">
    <span class="text-lg leading-tight font-semibold">{formatDuration(itinerary.duration)}</span>
    {#if left}
        <span class="rounded-full bg-amber-100 px-2 py-0.5 text-xs font-semibold text-amber-900 print:hidden"
            >Already left</span
        >
    {/if}
    {#if fastest}
        <span class="rounded-full bg-sky-100 px-2 py-0.5 text-xs font-semibold text-sky-900 print:hidden"
            >Fastest</span
        >
    {/if}
</p>
<div class="max-w-full min-w-44" style:width="{(itinerary.duration / longest) * 100}%">
    <p class="mt-1 mb-1 flex justify-between gap-3 text-sm font-medium tabular-nums">
        <time datetime={itinerary.depart}>{formatTime(itinerary.depart)}</time>
        <span class="sr-only">to</span>
        <time datetime={itinerary.arrive}>
            {formatTime(itinerary.arrive)}
            {#if laterDays > 0}
                <sup class="font-normal text-slate-600">+{laterDays}</sup>
            {/if}
        </time>
    </p>
    <!-- The steps of the trip say the same in words. -->
    <div class="relative" aria-hidden="true" onpointerover={showTip} onpointerleave={() => (tip = undefined)}>
        <div class="bar">
            {#each parts as { step, kind, seconds, widths }, index (index)}
                {@const Icon = KINDS[kind].icon}
                <span
                    class={["part", KINDS[kind].color]}
                    style:flex-grow={seconds}
                    style:--text={widths.text.toFixed(1)}
                    style:--both={widths.both?.toFixed(1)}
                    style:--names={widths.names?.toFixed(1)}
                    data-part={index}
                >
                    <span class="top">
                        <Icon class="size-4 shrink-0" />
                        {#if step.from && step.to}
                            <span class="long">{shortName(step.from)} → {shortName(step.to)}</span>
                        {/if}
                    </span>
                    <span class="text">
                        {#if step.from && step.to}
                            <span class="short">{step.from} → {step.to}</span>
                            <span class="dot">&nbsp;·&nbsp;</span>
                            <span class="time">{formatDuration(seconds)}</span>
                        {:else}
                            {formatDuration(seconds)}
                        {/if}
                    </span>
                </span>
            {/each}
        </div>
        {#if tip}
            <div
                class="pointer-events-none absolute bottom-full z-10 mb-1.5 w-max max-w-[min(22rem,100vw-1rem)] rounded-lg bg-slate-900 px-3 py-2 text-xs text-white shadow-lg"
                style:left="{Math.max(tip.min, Math.min(tip.center - tipWidth / 2, tip.max - tipWidth))}px"
                bind:offsetWidth={tipWidth}
            >
                <p class="font-semibold">{tip.part.step.description}</p>
                <p class="mt-0.5 tabular-nums">
                    {formatTime(tip.part.step.start)}
                    –
                    {formatTime(tip.part.step.end)}
                    · {formatDuration(tip.part.seconds)}
                </p>
            </div>
        {/if}
    </div>
</div>
{#if showSailings}
    <p class="mt-2 text-sm text-slate-600">
        {sailings.join(", ") || "No ferry"}
        {#if itinerary.drivingDistance > 0}
            · {formatDistance(itinerary.drivingDistance)} driving
        {/if}
    </p>
{/if}

<style>
.bar {
    display: flex;
    gap: 1px;
    height: 3rem;
    overflow: hidden;
    border-radius: 0.5rem;
    print-color-adjust: exact;
}

/*
 * Each part is as wide as its share of the time, and shows as much about itself as fits: its icon, then how long
 * it takes or the terminals of its sailing below, then both, then the terminals by name beside the icon.
 *
 * Whether a part is at least as wide as a width is told by a length that is less than nothing below the width
 * and more than any other from it on. Size container queries would say the same more plainly, but Firefox
 * does not apply them when printing.
 */
.part {
    /* What a part says is as wide as its letters, which are counted, and the space on either side of them. */
    --fits-icon: calc((100% - 1.25rem) * 999);
    --fits-text: calc((100% - var(--text) * 1em - 0.75rem) * 999);
    --fits-both: calc((100% - var(--both) * 1em - 0.75rem) * 999);
    --fits-names: calc((100% - var(--names) * 1em - 0.75rem) * 999);
    --lacks-names: calc((var(--names) * 1em + 0.75rem - 100%) * 999);

    display: flex;
    flex-basis: 0;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-width: 0;
    overflow: hidden;
    font-size: 0.75rem;
    line-height: 1;
    white-space: nowrap;
}

.top {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    max-width: clamp(0px, var(--fits-icon), 100%);
    padding: 0 clamp(0px, var(--fits-icon), 0.25rem);
    overflow: hidden;
}

/* The line of text is as tall as nothing until it fits, so that an icon alone is in the middle of its part. */
.text {
    display: flex;
    align-items: flex-start;
    justify-content: center;
    width: 100%;
    height: 0;
    padding: clamp(0px, var(--fits-text), 0.25rem) 0.25rem clamp(0px, var(--fits-text), 0.75rem);
    overflow: hidden;
}

.short,
.long,
.dot,
.time {
    flex-shrink: 0;
    overflow: hidden;
}

.short,
.long {
    font-weight: 600;
}

.long {
    flex-shrink: 1;
    max-width: clamp(0px, var(--fits-names), 100%);
    margin-left: clamp(0px, var(--fits-names), 0.25rem);
    text-overflow: ellipsis;
}

.short {
    max-width: clamp(0px, var(--lacks-names), 100%);
}

.dot {
    max-width: min(clamp(0px, var(--fits-both), 100%), clamp(0px, var(--lacks-names), 100%));
}

.time {
    max-width: clamp(0px, var(--fits-both), 100%);
}
</style>
