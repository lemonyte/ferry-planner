<script lang="ts">
import Results from "#lib/components/Results.svelte";
import SearchForm from "#lib/components/SearchForm.svelte";
import { formatDay } from "#lib/format.ts";
import { placeName } from "#lib/locations.ts";

let { data } = $props();

const { query } = $derived(data);
const searched = $derived(query.from !== "" && query.to !== "");
const title = $derived(
    searched
        ? `${placeName(query.from)} to ${placeName(query.to)} · ${formatDay(query.date)} · Ferry Planner`
        : "Ferry Planner",
);
</script>

<svelte:head>
    <title>{title}</title>
    <meta name="description" content="Find the best way between two places in British Columbia by BC Ferries.">
</svelte:head>

{#if !searched}
    <h1 class="mb-4 text-2xl font-bold">Plan a trip by ferry in British Columbia</h1>
{/if}

<SearchForm {query} />

{#await data.outcome}
    <p class="mt-6 text-slate-600" role="status">Getting the schedules…</p>
{:then outcome}
    {#if outcome.error}
        <p class="mt-4 rounded-xl border border-amber-300 bg-amber-50 p-4" role="alert">{outcome.error}</p>
    {:else if outcome.result}
        <Results {query} result={outcome.result} />
    {/if}
{/await}
