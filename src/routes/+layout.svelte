<script lang="ts">
    import "./layout.css";
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

<div class="flex min-h-dvh flex-col bg-slate-50 text-slate-900 print:bg-white">
    <p class="bg-sky-900 px-4 text-center text-sm text-sky-100 print:hidden">
        Found this helpful?
        <a
            href="https://github.com/sponsors/lemonyte"
            class="inline-flex min-h-10 items-center font-semibold text-white underline"
            target="_blank"
            rel="noopener"
        >
            Support Ferry Planner
        </a>
    </p>
    <header class="border-b border-slate-200 bg-white print:hidden">
        <nav class="mx-auto flex max-w-3xl items-center gap-1 px-4">
            <a href="/" class="mr-auto flex min-h-12 items-center text-lg font-bold">Ferry Planner</a>
            <a href="/about" class="flex min-h-12 items-center pl-3 text-slate-700 hover:text-slate-950"> About </a>
        </nav>
    </header>
    <main class="mx-auto w-full max-w-3xl flex-1 px-4 py-4 sm:py-8">
        {@render children()}
    </main>
    <footer class="border-t border-slate-200 print:hidden">
        <div class="mx-auto flex max-w-3xl flex-wrap items-center justify-between gap-x-4 px-4 text-sm text-slate-600">
            {#if downloaded || !schedules.online}
                <p class="w-full pt-2" role="status">
                    {#if !schedules.online}
                        <span class="font-semibold text-slate-900">Offline.</span>
                    {/if}
                    {downloaded ? `Schedules downloaded ${downloaded}.` : "No schedules downloaded yet."}
                </p>
            {/if}
            <p class="py-2">Not affiliated with BC Ferries.</p>
            <a
                href="https://github.com/lemonyte/ferry-planner"
                class="flex min-h-11 items-center underline hover:text-slate-950"
            >
                Source code on GitHub
            </a>
        </div>
    </footer>
</div>
