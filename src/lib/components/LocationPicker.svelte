<script lang="ts">
    import { Combobox } from "bits-ui";
    import { flushSync } from "svelte";

    import { filterPlaces, placeName } from "#lib/locations.ts";
    import { cities, locations, terminals } from "#lib/planner/data/locations.ts";

    interface Props {
        /** Form field name for the ID of the selected place. */
        name: string;
        label: string;
        /** ID of the selected place. */
        value: string;
    }

    let { name, label, value = $bindable() }: Props = $props();
    const id = $props.id();

    let open = $state(false);
    let typed = $state("");
    let list = $state<HTMLElement | null>(null);
    let input = $state<HTMLInputElement | null>(null);
    const groups = $derived(
        [
            { heading: "Cities and towns", places: filterPlaces(cities, typed) },
            { heading: "Ferry terminals", places: filterPlaces(terminals, typed) },
        ].filter((group) => group.places.length > 0),
    );
</script>

<Combobox.Root
    type="single"
    {name}
    bind:value
    bind:open
    required
    inputValue={placeName(value)}
    onOpenChangeComplete={(open) => {
        if (!open) {
            // Tab closes the list without selecting, so select the place whose name is typed in full.
            const text = input?.value.trim().toLowerCase();
            const match = Object.values(locations).find((place) => place.name.toLowerCase() === text);
            if (match) {
                value = match.id;
            }
            typed = "";
        }
    }}
>
    <div>
        <label for={id} class="field-label">{label}</label>
        <Combobox.Input
            {id}
            bind:ref={input}
            class="field pr-16 placeholder:text-stone-400 sm:pr-3"
            placeholder="{label}: city or terminal"
            defaultValue={placeName(value)}
            autocomplete="off"
            enterkeyhint="search"
            oninput={(event) => {
                typed = event.currentTarget.value;
                // bits-ui highlights the first item in view, so scroll the filtered list to the top first.
                flushSync();
                list?.scrollTo({ top: 0 });
            }}
            onfocus={(event) => event.currentTarget.select()}
            // bits-ui opens the list only when a key is pressed.
            onclick={() => (open = true)}
        />
    </div>
    <Combobox.Portal>
        <Combobox.Content
            class="z-10 max-h-[min(var(--bits-combobox-content-available-height),22rem)] w-(--bits-combobox-anchor-width) overflow-y-auto rounded-lg border border-stone-300 bg-white py-1 shadow-lg"
            sideOffset={4}
        >
            <Combobox.Viewport bind:ref={list}>
                {#each groups as group (group.heading)}
                    <Combobox.Group>
                        <Combobox.GroupHeading class="px-3 pt-2 pb-1 text-xs font-semibold text-stone-500 uppercase">
                            {group.heading}
                        </Combobox.GroupHeading>
                        {#each group.places as place (place.id)}
                            <Combobox.Item
                                class="flex min-h-11 cursor-pointer items-baseline justify-between gap-3 px-3 py-2 data-highlighted:bg-sea-100"
                                value={place.id}
                                label={place.name}
                            >
                                <span>{place.name}</span>
                                <span class="shrink-0 text-right text-xs text-stone-500">{place.region}</span>
                            </Combobox.Item>
                        {/each}
                    </Combobox.Group>
                {:else}
                    <p class="px-3 py-3 text-sm text-stone-600">No place by that name.</p>
                {/each}
            </Combobox.Viewport>
        </Combobox.Content>
    </Combobox.Portal>
</Combobox.Root>
