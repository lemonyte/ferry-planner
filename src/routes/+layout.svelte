<script lang="ts">
    import "./layout.css";
    import Ship from "@lucide/svelte/icons/ship";
    import { onMount } from "svelte";

    import { formatDay } from "#lib/format.ts";
    import { formatLocal, toLocal } from "#lib/planner/time.ts";
    import { schedules, watchSchedules } from "#lib/schedules.svelte.ts";

    let { children } = $props();

    // Day in British Columbia when the schedules in use were downloaded.
    const downloaded = $derived(
        schedules.fetchedAt === undefined ? undefined : formatDay(formatLocal(toLocal(schedules.fetchedAt))),
    );

    onMount(watchSchedules);
</script>

<div class="flex min-h-dvh flex-col bg-paper text-stone-900 print:bg-white">
    <header class="relative mb-2 bg-sea-900 text-white print:hidden">
        <nav class="mx-auto flex max-w-3xl items-center gap-1 px-4">
            <a href="/" class="heading mr-auto flex min-h-14 items-center gap-2 text-2xl">
                <Ship class="size-6 text-amber-300" strokeWidth={2.25} />
                Ferry Planner
            </a>
            <a href="/about" class="flex min-h-14 items-center pl-3 font-medium text-sea-100 hover:text-white">
                About
            </a>
        </nav>
        <div class="wave absolute inset-x-0 top-full bg-sea-900"></div>
    </header>
    <main class="mx-auto w-full max-w-3xl flex-1 px-4 py-4 sm:py-8">
        {@render children()}
    </main>
    <footer class="border-t border-stone-200 bg-white print:hidden">
        <div class="mx-auto flex max-w-3xl flex-wrap items-center justify-between gap-x-4 px-4 text-sm text-stone-600">
            {#if downloaded || !schedules.online}
                <p class="w-full pt-2" role="status">
                    {#if !schedules.online}
                        <span class="font-semibold text-stone-900">Offline.</span>
                    {/if}
                    {downloaded ? `Schedules downloaded ${downloaded}.` : "No schedules downloaded yet."}
                </p>
            {/if}
            <p class="py-2">Not affiliated with BC Ferries.</p>
            <a
                href="https://github.com/lemonyte/ferry-planner"
                class="flex min-h-11 items-center underline hover:text-stone-950"
            >
                Source code on GitHub
            </a>
        </div>
    </footer>
</div>
