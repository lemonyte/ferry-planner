import { createScheduledController } from "cloudflare:test";
import { env, exports } from "cloudflare:workers";
import { afterEach, expect, test, vi } from "vitest";
import worker from "../src/index";
import { FEED } from "./fixtures";
import plans from "./fixtures/plans.json";

// The worker always uses the same planner, which keeps its feed from one test to the next.
afterEach(() => {
    vi.restoreAllMocks();
});

const serveFeed = () => {
    return vi.spyOn(globalThis, "fetch").mockImplementation(async () => new Response(FEED));
};

const post = (path: string, body: unknown): Promise<Response> => {
    return exports.default.fetch(`https://ferryplanner.ca${path}`, { method: "POST", body: JSON.stringify(body) });
};

test("locations are all listed by ID", async () => {
    const response = await exports.default.fetch("https://ferryplanner.ca/api/locations");

    expect(response.status).toBe(200);
    expect(response.headers.get("Content-Type")).toBe("application/json");
    const locations = await response.json<Record<string, { id: string; name: string }>>();
    expect(Object.keys(locations)).toHaveLength(173);
    expect(locations.TSA).toMatchObject({
        id: "TSA",
        name: "Tsawwassen Terminal",
        coordinates: "49.006875,-123.130335",
    });
    expect(locations.victoria).toEqual({
        id: "victoria",
        name: "Victoria",
        region: "Vancouver Island",
        land_group: "Vancouver Island",
        province: "BC",
        country: "Canada",
    });
});

test("route plans are the same as from the Python planner", async () => {
    serveFeed();
    const expected = plans.find(({ request }) => request.origin === "HSB" && request.destination === "NAN");

    const response = await post("/api/routeplans", expected?.request);

    expect(response.status).toBe(200);
    expect((await response.json<{ hash: string }[]>()).map((plan) => plan.hash.slice(0, 12))).toEqual(
        expected?.hashes,
    );
});

test("schedule is for the terminals and date asked for", async () => {
    serveFeed();

    const response = await post("/api/ferry_schedule", { origin: "TSA", destination: "SWB", date: "2026-10-08" });

    expect(response.status).toBe(200);
    expect(await response.json()).toMatchObject({
        origin: "TSA",
        destination: "SWB",
        date: "2026-10-08T00:00:00",
        // Fifteen straight across, and one that calls at three islands on its way.
        sailings: expect.objectContaining({ length: 16 }),
    });
});

// Vancouver to Van Anda takes three ferries, by way of the Sunshine Coast or Vancouver Island.
const VAN_ANDA = "origin=vancouver&destination=van_anda&date=2026-10-08";

const search = async (query: string) => {
    // Midnight in Vancouver, before anything has left.
    vi.spyOn(Date, "now").mockReturnValue(Date.UTC(2026, 9, 8, 7));
    const response = await exports.default.fetch(`https://ferryplanner.ca/api/search?${query}`);
    expect(response.status).toBe(200);
    return response.json<{
        itineraries: { id: string; steps: { kind: string; from?: string; to?: string }[] }[];
        moreRoutes: number;
    }>();
};

test("search for a journey over several ferries has the itineraries of the route worth taking", async () => {
    serveFeed();

    const found = await search(VAN_ANDA);

    expect(
        found.itineraries.map((itinerary) =>
            itinerary.steps
                .filter((step) => step.kind === "FERRY")
                .map((step) => `${step.from}>${step.to}`)
                .join(" "),
        ),
    ).toEqual(Array(4).fill("HSB>LNG ERL>SLT PWR>TEX"));
    expect(found.moreRoutes).toBe(8);
});

test("search for all routes has the itineraries of the rest as well", async () => {
    serveFeed();

    const found = await search(`${VAN_ANDA}&routes=all`);

    expect(found.itineraries.length).toBeGreaterThan(4);
    expect(found.moreRoutes).toBe(0);
});

test("itinerary of a search is found by its ID", async () => {
    serveFeed();
    const [itinerary] = (await search(VAN_ANDA)).itineraries;

    const response = await exports.default.fetch(
        `https://ferryplanner.ca/api/itinerary?${VAN_ANDA}&id=${itinerary?.id}`,
    );

    expect(response.status).toBe(200);
    expect(await response.json()).toEqual(itinerary);
});

test.each(["/", "/api", "/api/routes", "/api/routeplans/"])("nothing is found at %s", async (path) => {
    const response = await exports.default.fetch(`https://ferryplanner.ca${path}`);

    expect(response.status).toBe(404);
    expect(await response.json()).toEqual({ detail: "Not Found" });
});

test.each([
    ["POST", "/api/locations"],
    ["GET", "/api/routeplans"],
    ["GET", "/api/ferry_schedule"],
    ["POST", "/api/search"],
    ["POST", "/api/itinerary"],
])("%s is not allowed at %s", async (method, path) => {
    const fetch = serveFeed();

    const response = await exports.default.fetch(`https://ferryplanner.ca${path}`, { method });

    expect(response.status).toBe(405);
    expect(await response.json()).toEqual({ detail: "Method Not Allowed" });
    expect(fetch).not.toHaveBeenCalled();
});

test("feed is downloaded on schedule", async () => {
    const fetch = serveFeed();

    await worker.scheduled(createScheduledController(), env);

    expect(fetch).toHaveBeenCalledTimes(1);
});
