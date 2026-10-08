import adapter from "@sveltejs/adapter-cloudflare";
import { sveltekit } from "@sveltejs/kit/vite";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vitest/config";

export default defineConfig({
    plugins: [
        tailwindcss(),
        sveltekit({
            compilerOptions: {
                // Force runes mode for the project, except for libraries. Can be removed in svelte 6.
                runes: ({ filename }) => (filename.split(/[/\\]/).includes("node_modules") ? undefined : true),
            },
            adapter: adapter(),
        }),
    ],
    // Lets tests import the feed archive in `test/fixtures`.
    assetsInclude: ["**/*.zip"],
    test: {
        expect: { requireAssertions: true },
        environment: "node",
        include: ["src/**/*.test.ts"],
    },
});
