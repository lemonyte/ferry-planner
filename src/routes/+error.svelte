<script lang="ts">
import { page } from "$app/state";
</script>

<svelte:head>
    <title>{page.status === 404 ? "Not found" : "Not available"} · Ferry Planner</title>
</svelte:head>

<div class="rounded-xl border border-amber-300 bg-amber-50 p-4" role="alert">
    <p>{page.error?.message}</p>
    <!-- A link to a trip has the search that it is from, to look for it again. -->
    <a
        class="mt-3 inline-flex min-h-11 items-center rounded-lg bg-sky-700 px-4 font-semibold text-white hover:bg-sky-800"
        href="/{page.route.id === "/trip/[id]" ? page.url.search : ""}"
    >
        {page.route.id === "/trip/[id]" ? "Search again" : "Plan a trip"}
    </a>
</div>
