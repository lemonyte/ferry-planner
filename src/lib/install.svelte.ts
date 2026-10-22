/** Install prompt of Chromium-based browsers, which they fire only while the site is installable and not installed. */
type InstallPrompt = Event & { prompt: () => Promise<unknown> };

export const install = $state<{ prompt?: InstallPrompt; ios: boolean }>({ ios: false });

/**
 * Check if a browser is on iOS or iPadOS and the site is not opened from the Home Screen. Browsers there have no
 * install prompt, so the visitor adds the site from the Share menu. This covers Safari and Chrome, which both report iOS.
 */
export const canAddToHomeScreen = (userAgent: string, maxTouchPoints: number, standalone: boolean): boolean => {
    // iPadOS reports the user agent of macOS, which has no touch screen.
    const ios = /iPhone|iPad|iPod/.test(userAgent) || (/Macintosh/.test(userAgent) && maxTouchPoints > 1);
    return ios && !standalone;
};

/** Keep the install prompt for later use. Returns a function that stops listening. */
export const watchInstall = (): (() => void) => {
    const standalone =
        (navigator as { standalone?: boolean }).standalone === true || matchMedia("(display-mode: standalone)").matches;
    install.ios = canAddToHomeScreen(navigator.userAgent, navigator.maxTouchPoints, standalone);
    const stop = new AbortController();
    window.addEventListener(
        "beforeinstallprompt",
        (event) => {
            event.preventDefault();
            install.prompt = event as InstallPrompt;
        },
        stop,
    );
    window.addEventListener("appinstalled", () => (install.prompt = undefined), stop);
    return () => stop.abort();
};

/** Show the install prompt of the browser. A prompt can be shown only once. */
export const promptInstall = async (): Promise<void> => {
    const prompt = install.prompt;
    install.prompt = undefined;
    await prompt?.prompt();
};
