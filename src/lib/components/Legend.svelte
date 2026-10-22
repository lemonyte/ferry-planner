<script lang="ts">
    import { STEP_KINDS } from "#lib/steps.ts";
</script>

<ul class="flex flex-wrap gap-x-4 gap-y-1 text-sm text-stone-600" aria-label="Colours of the bars">
    {#each Object.values(STEP_KINDS) as kind (kind.label)}
        <li class="flex items-center gap-1.5">
            <span class={["flex size-5 items-center justify-center rounded", kind.bar]}>
                <kind.icon class="size-3.5" />
            </span>
            {kind.label}
        </li>
    {/each}
</ul>
