<script lang="ts">
import { Combobox } from "bits-ui";
import { CITIES, filterPlaces, placeName, TERMINALS } from "#lib/locations.ts";

interface Props {
    /** Name that the ID of the place picked is submitted under. */
    name: string;
    label: string;
    /** ID of the place picked. */
    value: string;
}

let { name, label, value = $bindable() }: Props = $props();
const id = $props.id();

let typed = $state("");
const groups = $derived(
    [
        { heading: "Cities and towns", places: filterPlaces(CITIES, typed) },
        { heading: "Ferry terminals", places: filterPlaces(TERMINALS, typed) },
    ].filter((group) => group.places.length > 0),
);
</script>

<Combobox.Root
    type="single"
    {name}
    bind:value
    required
    inputValue={placeName(value)}
    onOpenChangeComplete={(open) => {
        if (!open) {
            typed = "";
        }
    }}
>
    <div>
        <label for={id} class="sr-only text-sm font-medium text-slate-700 sm:not-sr-only sm:mb-1 sm:block"
            >{label}</label
        >
        <Combobox.Input
            {id}
            class="h-12 w-full rounded-lg border border-slate-300 bg-white pr-16 pl-3 text-base placeholder:text-slate-400 sm:pr-3"
            placeholder="{label}: city or terminal"
            defaultValue={placeName(value)}
            autocomplete="off"
            enterkeyhint="search"
            oninput={(event) => {
                typed = event.currentTarget.value;
            }}
            onfocus={(event) => event.currentTarget.select()}
        />
    </div>
    <Combobox.Portal>
        <Combobox.Content
            class="z-10 max-h-[min(var(--bits-combobox-content-available-height),22rem)] w-(--bits-combobox-anchor-width) overflow-y-auto rounded-lg border border-slate-300 bg-white py-1 shadow-lg"
            sideOffset={4}
        >
            <Combobox.Viewport>
                {#each groups as group (group.heading)}
                    <Combobox.Group>
                        <Combobox.GroupHeading class="px-3 pt-2 pb-1 text-xs font-semibold text-slate-500 uppercase">
                            {group.heading}
                        </Combobox.GroupHeading>
                        {#each group.places as place (place.id)}
                            <Combobox.Item
                                class="flex min-h-11 cursor-pointer items-baseline justify-between gap-3 px-3 py-2 data-highlighted:bg-sky-100"
                                value={place.id}
                                label={place.name}
                            >
                                <span>{place.name}</span>
                                <span class="shrink-0 text-right text-xs text-slate-500">{place.region}</span>
                            </Combobox.Item>
                        {/each}
                    </Combobox.Group>
                {:else}
                    <p class="px-3 py-3 text-sm text-slate-600">No place by that name.</p>
                {/each}
            </Combobox.Viewport>
        </Combobox.Content>
    </Combobox.Portal>
</Combobox.Root>
