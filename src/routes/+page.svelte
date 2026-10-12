<script lang="ts">
    import { onMount } from "svelte";

    import Head from "#lib/components/Head.svelte";
    import Legend from "#lib/components/Legend.svelte";
    import PopularRoutes from "#lib/components/PopularRoutes.svelte";
    import SearchForm from "#lib/components/SearchForm.svelte";
    import TripList from "#lib/components/TripList.svelte";
    import TripSummary from "#lib/components/TripSummary.svelte";
    import { EXAMPLE_TRIP } from "#lib/example.ts";
    import { formatDay } from "#lib/format.ts";
    import { placeName } from "#lib/locations.ts";
    import { DESCRIPTION, ORIGIN, SITE_NAME } from "#lib/site.ts";

    let { data } = $props();

    const { query } = $derived(data);
    const searched = $derived(query.from !== "" && query.to !== "");
    const title = $derived(
        searched
            ? `${placeName(query.from)} to ${placeName(query.to)} · ${formatDay(query.date)} · ${SITE_NAME}`
            : `${SITE_NAME} · BC Ferries trip planner`,
    );

    // Escaped so that no text in it can close the script element.
    const structuredData = JSON.stringify({
        "@context": "https://schema.org",
        "@type": "WebApplication",
        name: SITE_NAME,
        url: `${ORIGIN}/`,
        description: DESCRIPTION,
        applicationCategory: "TravelApplication",
        operatingSystem: "Any",
        offers: { "@type": "Offer", price: "0", priceCurrency: "CAD" },
    }).replaceAll("<", String.raw`<`);

    onMount(() => {
        // Set by `src/app.html`. The page now shows what the URL asks for.
        delete document.documentElement.dataset.searched;
    });
</script>

<!-- Every search is the same page to a search engine. -->
<Head {title} description={DESCRIPTION} canonical="/" />

<svelte:head>
    {#if !searched}
        {@html `<script type="application/ld+json">${structuredData}</` + `script>`}
    {/if}
</svelte:head>

{#if !searched}
    <h1 class="intro heading mb-4 text-3xl">Plan a trip by ferry in British Columbia</h1>
{/if}

<SearchForm {query} />

{#await data.outcome}
    <p class="mt-6 text-stone-600" role="status">Getting the schedules…</p>
{:then outcome}
    {#if outcome.error}
        <p class="alert mt-4" role="alert">{outcome.error}</p>
    {:else if outcome.result}
        <TripList {query} result={outcome.result} />
    {/if}
{/await}

{#if !searched}
    <div class="intro">
        <section class="mt-8">
            <h2 class="heading text-xl">Every trip, door to door</h2>
            <p class="mt-1 leading-relaxed text-stone-700">
                Each trip counts the drive to the terminal, the wait at check-in, and every sailing, so you know when to
                leave and when you arrive.
            </p>
            <figure class="card-bleed mt-3 p-4">
                <figcaption class="mb-2 text-sm text-stone-600">Example: Vancouver to Powell River</figcaption>
                <TripSummary itinerary={EXAMPLE_TRIP} />
                <div class="mt-3"><Legend /></div>
            </figure>
        </section>
        <PopularRoutes heading="Popular routes" />
    </div>
{/if}
