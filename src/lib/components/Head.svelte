<script lang="ts">
    import { ORIGIN } from "#lib/site.ts";

    interface Props {
        title: string;
        description: string;
        /** Path of the page that search engines index for this content. Omit to keep the page out of search results. */
        canonical?: string;
    }

    let { title, description, canonical }: Props = $props();
</script>

<svelte:head>
    <title>{title}</title>
    <meta name="description" content={description} />
    {#if canonical}
        <link rel="canonical" href={ORIGIN + canonical} />
        <meta property="og:url" content={ORIGIN + canonical} />
        <meta property="og:title" content={title} />
        <meta property="og:description" content={description} />
    {:else}
        <!-- `src/hooks.server.ts` adds the title and description that link previews of these pages show. -->
        <meta name="robots" content="noindex" />
    {/if}
</svelte:head>
