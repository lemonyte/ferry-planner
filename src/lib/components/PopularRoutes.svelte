<script lang="ts">
    import { resolve } from "$app/paths";
    import ArrowRight from "@lucide/svelte/icons/arrow-right";

    import { placeName } from "#lib/locations.ts";
    import { POPULAR_ROUTES, routeSlug } from "#lib/popular.ts";

    interface Props {
        heading: string;
        /** Slug of a route to leave out. */
        except?: string;
    }

    let { heading, except }: Props = $props();
    const id = $props.id();

    const routes = $derived(POPULAR_ROUTES.filter((route) => routeSlug(route) !== except));
</script>

<nav class="mt-8 print:hidden" aria-labelledby={id}>
    <h2 {id} class="heading text-xl">{heading}</h2>
    <ul class="mt-3 grid gap-2 sm:grid-cols-2">
        {#each routes as route (routeSlug(route))}
            <li>
                <a
                    class="card flex min-h-12 items-center justify-between gap-3 px-4 font-medium hover:border-sea-600 hover:text-sea-800"
                    href={resolve("/routes/[route]", { route: routeSlug(route) })}
                >
                    {placeName(route.from)} to {placeName(route.to)}
                    <ArrowRight class="size-4.5 shrink-0 text-sea-700" />
                </a>
            </li>
        {/each}
    </ul>
</nav>
