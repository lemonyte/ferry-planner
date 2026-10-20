<script lang="ts">
    import Head from "#lib/components/Head.svelte";
    import { SITE_NAME } from "#lib/site.ts";
</script>

<Head
    title="About · {SITE_NAME}"
    description="What {SITE_NAME} does, how it plans a trip by BC Ferries, and where its schedules come from."
    canonical="/about"
/>

<article class="space-y-4 leading-relaxed">
    <h1 class="heading text-3xl">About</h1>
    <p>
        Ferry Planner finds ways to travel between places in British Columbia that need a
        <a class="underline" href="https://www.bcferries.com">BC Ferries</a>
        sailing. Pick where you are leaving from, where you are going, and a day, and it shows the best routes to take with
        the sailings you can catch.
    </p>
    <p>
        Each itinerary allows for the drive to the terminal, the time that check-in closes before a sailing, and the
        wait for the next sailing where a journey takes more than one ferry.
    </p>
    <p>
        Sailing times come from the schedule that BC Ferries publishes. It is downloaded to your device and checked for
        changes when you open or come back to the site, so trips can be found without an Internet connection once the
        site has been opened with one. Driving times are estimates.
    </p>
    <h2 class="heading text-2xl">Disclaimer</h2>
    <p>
        Ferry Planner is not affiliated with BC Ferries. Ferry Planner provides information on a best-effort basis and
        does not guarantee correct or up-to-date results. Delays, cancellations, full sailings, and other exceptions
        such as foot-passenger-only sailings are not known to this site, so check with BC Ferries before you travel.
        Ferry Planner and its developers assume no liability for any consequences related to its use such as, but not
        limited to, missed sailings and lost funds.
    </p>
</article>
