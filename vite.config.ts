import adapter from "@sveltejs/adapter-cloudflare";
import { sveltekit } from "@sveltejs/kit/vite";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vitest/config";

export default defineConfig({
    plugins: [
        tailwindcss(),
        sveltekit({
            adapter: adapter(),
            // The service worker serves the prerendered app shell at any path, so its links cannot be relative.
            paths: { relative: false },
        }),
    ],
    test: {
        expect: { requireAssertions: true },
        environment: "node",
        include: ["src/**/*.test.ts"],
    },
});
