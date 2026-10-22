<script lang="ts">
    import Download from "@lucide/svelte/icons/download";
    import Heart from "@lucide/svelte/icons/heart";

    import { install, promptInstall } from "#lib/install.svelte.ts";
</script>

<div class="mt-6 grid gap-3 sm:auto-cols-fr sm:grid-flow-col print:hidden">
    <p class="card flex gap-3 p-4 text-sm text-stone-700">
        <Heart class="mt-1.5 size-5 shrink-0 text-amber-500" />
        <span>
            Found this helpful?
            <a class="link font-medium" href="https://github.com/sponsors/lemonyte" target="_blank" rel="noopener">
                Support Ferry Planner
            </a>
        </span>
    </p>
    {#if install.prompt || install.ios}
        <p class="card flex gap-3 p-4 text-sm text-stone-700">
            <Download class="mt-1.5 size-5 shrink-0 text-sea-700" />
            <span>
                Look up sailings without a connection.
                {#if install.prompt}
                    <button type="button" class="link font-medium" onclick={promptInstall}>
                        Install Ferry Planner
                    </button>
                {:else}
                    Open the Share menu, then choose Add to Home Screen.
                {/if}
            </span>
        </p>
    {/if}
</div>
