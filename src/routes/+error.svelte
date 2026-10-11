<script lang="ts">
    import { page } from "$app/state";
</script>

<svelte:head>
    <title>{page.status === 404 ? "Not found" : "Not available"} · Ferry Planner</title>
</svelte:head>

<div class="alert" role="alert">
    <p>{page.error?.message}</p>
    <a class="btn btn-primary mt-3" href="/{page.route.id === '/trip/[id]' ? page.url.search : ''}">
        {page.route.id === "/trip/[id]" ? "Search again" : "Plan a trip"}
    </a>
</div>
