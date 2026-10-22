import { expect, test } from "vitest";

import { canAddToHomeScreen } from "./install.svelte.ts";

const SAFARI_IPHONE =
    "Mozilla/5.0 (iPhone; CPU iPhone OS 26_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 Mobile/15E148 Safari/604.1";
const CHROME_IPHONE =
    "Mozilla/5.0 (iPhone; CPU iPhone OS 26_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/141.0.7390.41 Mobile/15E148 Safari/604.1";
const SAFARI_IPAD =
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 Safari/605.1.15";
const CHROME_ANDROID =
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36";

test("canAddToHomeScreen is true for Safari and Chrome on an iPhone", () => {
    expect(canAddToHomeScreen(SAFARI_IPHONE, 5, false)).toBe(true);
    expect(canAddToHomeScreen(CHROME_IPHONE, 5, false)).toBe(true);
});

test("canAddToHomeScreen is true for an iPad, which reports macOS", () => {
    expect(canAddToHomeScreen(SAFARI_IPAD, 5, false)).toBe(true);
});

test("canAddToHomeScreen is false for macOS, Android, and a site opened from the Home Screen", () => {
    expect(canAddToHomeScreen(SAFARI_IPAD, 0, false)).toBe(false);
    expect(canAddToHomeScreen(CHROME_ANDROID, 5, false)).toBe(false);
    expect(canAddToHomeScreen(SAFARI_IPHONE, 5, true)).toBe(false);
});
