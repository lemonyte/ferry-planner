<script lang="ts">
    import { daysBetween, formatDistance, formatDuration, formatTime, secondsBetween } from "#lib/format.ts";
    import type { Itinerary, Step } from "#lib/planner/itinerary.ts";
    import { STEP_KINDS, sailingName } from "#lib/steps.ts";

    interface Props {
        itinerary: Itinerary;
        /** Duration in seconds of the longest trip shown. Bar widths are proportional to it. */
        longest?: number;
        /** Whether this is the fastest trip shown. */
        fastest?: boolean;
        /** Whether the trip has already departed. */
        left?: boolean;
    }

    let { itinerary, longest = itinerary.duration, fastest = false, left = false }: Props = $props();

    // Estimated character widths in ems, rounded up so that text reported to fit does fit.
    const BOLD_WIDTH = 0.68;
    const PLAIN_WIDTH = 0.58;

    interface Part {
        step: Step;
        kind: keyof typeof STEP_KINDS;
        seconds: number;
        /** Widths in ems of the text a part can show: the shortest, the shortest with the duration, and the terminal names. */
        widths: { text: number; both?: number; names?: number };
    }

    const toWidths = (step: Step, seconds: number): Part["widths"] => {
        const time = formatDuration(seconds).length * PLAIN_WIDTH;
        const sailing = sailingName(step);
        if (!sailing) {
            return { text: time };
        }
        const codes = `${step.from} → ${step.to}`.length * BOLD_WIDTH;
        const names = sailing.length * BOLD_WIDTH;
        // The names sit beside the icon, which is 1.75 em wide with its gap.
        return { text: codes, both: codes + 3 * PLAIN_WIDTH + time, names: Math.max(names + 1.75, time) };
    };

    const parts = $derived(
        itinerary.steps.flatMap((step): Part[] => {
            const seconds = secondsBetween(step.start, step.end);
            return step.kind !== "MARK" && seconds > 0
                ? [{ step, kind: step.kind, seconds, widths: toWidths(step, seconds) }]
                : [];
        }),
    );
    const laterDays = $derived(daysBetween(itinerary.depart, itinerary.arrive));

    /** Bar part under the pointer, and the tooltip position in pixels from the left of the bar. */
    let tip = $state<{ part: Part; center: number; min: number; max: number }>();
    let tipWidth = $state(0);

    const showTip = (event: PointerEvent & { currentTarget: HTMLElement }) => {
        const element = event.target instanceof Element ? event.target.closest<HTMLElement>("[data-part]") : null;
        const part = parts[Number(element?.dataset.part)];
        // Touch opens the trip page, which shows the same details.
        if (!element || !part || event.pointerType !== "mouse") {
            tip = undefined;
            return;
        }
        const bar = event.currentTarget.getBoundingClientRect();
        const box = element.getBoundingClientRect();
        tip = {
            part,
            center: box.left + box.width / 2 - bar.left,
            // Keep the tooltip within the page.
            min: 8 - bar.left,
            max: document.documentElement.clientWidth - 8 - bar.left,
        };
    };
</script>

<p class="flex flex-wrap items-center gap-x-2 gap-y-1 whitespace-nowrap">
    <span class="text-lg leading-tight font-semibold">{formatDuration(itinerary.duration)}</span>
    {#if left}
        <span class="badge bg-amber-100 text-amber-900 print:hidden">Already left</span>
    {/if}
    {#if fastest}
        <span class="badge bg-sky-100 text-sky-900 print:hidden">Fastest</span>
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
    <div class="relative" aria-hidden="true" onpointerover={showTip} onpointerleave={() => (tip = undefined)}>
        <div class="bar">
            {#each parts as { step, kind, seconds, widths }, index}
                {@const Icon = STEP_KINDS[kind].icon}
                {@const sailing = sailingName(step)}
                <span
                    class={["part", STEP_KINDS[kind].bar]}
                    style:flex-grow={seconds}
                    style:--text={widths.text.toFixed(1)}
                    style:--both={widths.both?.toFixed(1)}
                    style:--names={widths.names?.toFixed(1)}
                    data-part={index}
                >
                    <span class="top">
                        <Icon class="size-4 shrink-0" />
                        {#if sailing}
                            <span class="long">{sailing}</span>
                        {/if}
                    </span>
                    <span class="text">
                        {#if sailing}
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
{#if itinerary.drivingDistance > 0}
    <p class="mt-2 text-sm text-slate-600">
        {formatDistance(itinerary.drivingDistance)} driving
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
    * Each part is as wide as its share of the duration and shows as much as fits: the icon, then the duration or
    * the terminal codes below it, then both, then the terminal names beside the icon.
    *
    * Each `--fits-*` length is negative if the part is narrower than the text and very large otherwise, so
    * `clamp()` turns it into a toggle. Size container queries would be simpler, but Firefox does not apply
    * them when printing.
    */
    .part {
        /* Text width is its character count in ems plus padding. */
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
