import { cloudflareTest } from "@cloudflare/vitest-plugin";
import { defineConfig } from "vitest/config";

export default defineConfig({
    // Lets tests import the feed archive in `test/fixtures`.
    assetsInclude: ["**/*.zip"],
    plugins: [cloudflareTest({ wrangler: { configPath: "./wrangler.jsonc" } })],
});
