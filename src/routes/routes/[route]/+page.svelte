<script lang="ts">
    import { resolve } from "$app/paths";

    import Head from "#lib/components/Head.svelte";
    import PopularRoutes from "#lib/components/PopularRoutes.svelte";
    import { formatDistance, formatDuration } from "#lib/format.ts";
    import { shortName } from "#lib/locations.ts";
    import { SITE_NAME } from "#lib/site.ts";
    import { STEP_KINDS } from "#lib/steps.ts";

    let { data } = $props();

    const { from, to, ways } = $derived(data);

    const journey = $derived(`${from.name} to ${to.name}`);
    const COUNTS = ["no", "one", "two", "three"];

    /** Name the sailings of each way, each as `Horseshoe Bay to Langdale`. */
    const sailings = $derived(
        ways.map((way) => {
            return way.flatMap((step) => {
                return step.kind === "FERRY" ? `${shortName(step.depart.id)} to ${shortName(step.arrive.id)}` : [];
            });
        }),
    );
    const choice = $derived.by(() => {
        const described = sailings.map((names) => `from ${names.join(", then from ")}`);
        const [only] = sailings;
        if (only && sailings.length === 1) {
            const count = only.length === 1 ? "one BC Ferries sailing" : `${COUNTS[only.length]} BC Ferries sailings`;
            return `${count}, ${described[0]}`;
        }
        return `BC Ferries sailings one of ${COUNTS[sailings.length]} ways: ${described.join("; or ")}`;
    });
    // The date is left out of the link so that it is the day that the link is followed on.
    const search = $derived(`${resolve("/")}?${new URLSearchParams({ from: from.id, to: to.id })}`);
</script>

<Head
    title="{journey} by ferry · {SITE_NAME}"
    description="How to get from {journey} with {choice}: the drive to and from the terminals, when check-in closes, and the sailings for the day you travel."
    canonical="/routes/{data.slug}"
/>

<article>
    <h1 class="heading text-3xl">{journey} by ferry</h1>
    <p class="mt-3 leading-relaxed">
        Getting from {journey} takes {choice}. {SITE_NAME} works out when to leave, which sailing you can catch, and when
        you arrive.
    </p>
    <a class="btn btn-primary mt-4" href={search}>See the trips for today</a>

    {#each ways as way, index}
        <section class="card-bleed mt-6 p-4">
            <h2 class="font-display text-xl leading-snug font-semibold">
                {#each sailings[index] as sailing}
                    <span class="block">{sailing.replace(" to ", " → ")}</span>
                {/each}
            </h2>
            <ol class="mt-4 space-y-3 border-l-2 border-stone-200 pl-4">
                {#each way as step}
                    {#if step.kind === "DRIVE"}
                        <li class="relative">
                            <span class={["step-dot", STEP_KINDS.DRIVE.dot]}></span>
                            Drive from {step.from} to {step.to}
                            <span class="text-sm whitespace-nowrap text-stone-500">
                                · {formatDuration(step.seconds)}, {formatDistance(step.kilometres)}
                            </span>
                        </li>
                    {:else}
                        <li class="relative">
                            <span class={["step-dot", STEP_KINDS.WAIT.dot]}></span>
                            Check in at {step.depart.name}.
                            {#if step.reservationClose}
                                With a reservation, check-in closes {step.reservationClose} minutes before the sailing.
                            {/if}
                            <a class="link text-sm" href={step.depart.infoUrl} target="_blank" rel="noopener">
                                Terminal information from BC Ferries
                            </a>
                        </li>
                        <li class="relative">
                            <span class={["step-dot", STEP_KINDS.FERRY.dot]}></span>
                            Sail to {step.arrive.name}
                        </li>
                    {/if}
                {/each}
            </ol>
        </section>
    {/each}

    <p class="mt-4 text-sm leading-relaxed text-stone-600">
        Driving times are estimates. Sailing times change with the day and the season, so look up the day you are
        travelling. Other ways to make this trip, such as through other terminals, are listed with the trips.
    </p>
</article>

<PopularRoutes heading="Other popular routes" except={data.slug} />
