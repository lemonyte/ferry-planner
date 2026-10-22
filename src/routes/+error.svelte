<script lang="ts">
    import { page } from "$app/state";

    import Head from "#lib/components/Head.svelte";
    import { SITE_NAME } from "#lib/site.ts";
</script>

<Head
    title="{page.status === 404 ? 'Not found' : 'Not available'} · {SITE_NAME}"
    description={page.error?.message ?? ""}
/>

<div class="alert" role="alert">
    <p>{page.error?.message}</p>
    <a class="btn btn-primary mt-3" href="/{page.route.id === '/trip/[id]' ? page.url.search : ''}">
        {page.route.id === "/trip/[id]" ? "Search again" : "Plan a trip"}
    </a>
</div>
