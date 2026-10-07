import { evictDurableObject, runInDurableObject } from "cloudflare:test";
import { env } from "cloudflare:workers";
import { afterEach, expect, test, vi } from "vitest";
import { type FeedFiles, HSB_TO_LNG, makeArchive } from "./feeds";

const GTFS_URL = "https://data.trilliumtransit.com/gtfs/bcferries-bc-ca/bcferries-bc-ca.zip";
const BOTH_WAYS: FeedFiles = {
    trips: "r,daily,t\nr,daily,u\n",
    stopTimes: `${HSB_TO_LNG}u,09:00:00,09:00:00,2,1\nu,09:40:00,09:40:00,1,2\n`,
};

interface Schedule {
    sailings: { departure: string; arrival: string; duration: number; notes: string[] }[];
    notes: string[];
}

afterEach(() => {
    vi.restoreAllMocks();
});

/** Answer each download of the feed with the next of the given archives or statuses, repeating the last. */
const serve = (...contents: (Uint8Array | string | number | { body: Uint8Array | string; etag: string })[]) => {
    return vi.spyOn(globalThis, "fetch").mockImplementation(async () => {
        const content = contents.length > 1 ? contents.shift() : contents[0];
        // Lets the other requests that were made at once reach the planner during the download.
        await scheduler.wait(1);
        if (typeof content === "number") {
            return new Response(null, { status: content });
        }
        // The response is made here as the planner can only read one that was made while it is running.
        return typeof content === "object" && "etag" in content
            ? new Response(content.body, { headers: { ETag: content.etag } })
            : new Response(content);
    });
};

/** Get a planner that no other test uses, as planners keep what they store for all the tests in a file. */
const makePlanner = () => {
    return env.PLANNER.getByName(crypto.randomUUID());
};

const post = (planner: ReturnType<typeof makePlanner>, path: string, body: unknown): Promise<Response> => {
    return planner.fetch(`https://planner${path}`, { method: "POST", body: JSON.stringify(body) });
};

const getSchedule = (
    planner: ReturnType<typeof makePlanner>,
    origin: string,
    destination: string,
    date = "2026-10-06",
) => {
    return post(planner, "/api/ferry_schedule", { origin, destination, date });
};

test("schedule has the sailings from the feed", async () => {
    serve(makeArchive());

    const response = await getSchedule(makePlanner(), "HSB", "LNG");

    expect(response.status).toBe(200);
    expect(await response.json()).toEqual({
        date: "2026-10-06T00:00:00",
        origin: "HSB",
        destination: "LNG",
        sailings: [
            {
                departure: "2026-10-06T07:30:00-07:00",
                arrival: "2026-10-06T08:10:00-07:00",
                duration: 40 * 60,
                notes: [],
            },
        ],
        url: "https://www.bcferries.com/routes-fares/schedules/daily/HSB-LNG?&scheduleDate=10/06/2026",
        notes: [],
    });
});

test("schedule without a date is for today", async () => {
    serve(makeArchive());
    vi.spyOn(Date, "now").mockReturnValue(Date.UTC(2026, 9, 7, 3, 30));

    const response = await post(makePlanner(), "/api/ferry_schedule", { origin: "HSB", destination: "LNG" });

    // Half past three in the morning in UTC is the evening before in Vancouver.
    expect(await response.json()).toMatchObject({ date: "2026-10-06T20:30:00", sailings: [expect.anything()] });
});

test("schedule without sailings says so", async () => {
    serve(makeArchive());

    const schedule = await (await getSchedule(makePlanner(), "LNG", "HSB")).json<Schedule>();

    expect(schedule.sailings).toEqual([]);
    expect(schedule.notes).toEqual(["No sailings found"]);
});

test("schedule for a date the feed does not cover says so", async () => {
    serve(makeArchive({ feedInfo: "Publisher,20260101,20261005" }));

    const schedule = await (await getSchedule(makePlanner(), "HSB", "LNG")).json<Schedule>();

    expect(schedule.sailings).toEqual([]);
    expect(schedule.notes).toEqual(["Seasonal schedules have not been posted for these dates"]);
});

test("sailing that calls at terminals on the way names them", async () => {
    serve(makeArchive({ stopTimes: "t,07:30:00,07:30:00,1,1\nt,08:10:00,08:25:00,2,2\nt,10:00:00,10:00:00,3,3\n" }));

    const schedule = await (await getSchedule(makePlanner(), "HSB", "NAN")).json<Schedule>();

    expect(schedule.sailings.map((sailing) => sailing.notes)).toEqual([["Via Langdale Terminal"]]);
});

test("feed is downloaded once for several schedules", async () => {
    const fetch = serve(makeArchive());
    const planner = makePlanner();

    await Promise.all([getSchedule(planner, "HSB", "LNG"), getSchedule(planner, "LNG", "HSB")]);
    await getSchedule(planner, "HSB", "LNG", "2026-10-07");

    expect(fetch).toHaveBeenCalledTimes(1);
    expect(fetch).toHaveBeenCalledWith(GTFS_URL, { headers: {} });
});

test("feed is kept when the planner restarts", async () => {
    const fetch = serve(makeArchive());
    const planner = makePlanner();
    // The planner cannot be stopped while it has a response that has not been read.
    await (await getSchedule(planner, "HSB", "LNG")).json();

    await evictDurableObject(planner);
    const schedule = await (await getSchedule(planner, "HSB", "LNG")).json<Schedule>();

    expect(schedule.sailings).toHaveLength(1);
    expect(fetch).toHaveBeenCalledTimes(1);
});

test.each([
    ["cannot be downloaded", 503],
    ["is not a GTFS archive", "<html>Waiting room</html>"],
    // The stop sequences are missing.
    ["is malformed", makeArchive({ stopTimes: "t,07:30:00,07:30:00,1\nt,08:10:00,08:10:00,2\n" })],
])("no schedule when the feed %s", async (_, content) => {
    serve(content);

    const response = await getSchedule(makePlanner(), "HSB", "LNG");

    expect(response.status).toBe(404);
    expect(await response.json()).toEqual({ detail: "Schedule not found" });
});

test("failed download is not repeated for every schedule", async () => {
    const fetch = serve(503);
    const planner = makePlanner();

    const responses = await Promise.all([getSchedule(planner, "HSB", "LNG"), getSchedule(planner, "LNG", "HSB")]);
    responses.push(await getSchedule(planner, "HSB", "LNG", "2026-10-07"));

    expect(responses.map((response) => response.status)).toEqual([404, 404, 404]);
    expect(fetch).toHaveBeenCalledTimes(1);
});

test("feed is downloaded again a minute after a failed download", async () => {
    serve(503, makeArchive());
    const now = vi.spyOn(Date, "now").mockReturnValue(Date.UTC(2026, 9, 6, 12));
    const planner = makePlanner();
    expect((await getSchedule(planner, "HSB", "LNG")).status).toBe(404);

    now.mockReturnValue(Date.UTC(2026, 9, 6, 12, 1, 1));

    expect((await getSchedule(planner, "HSB", "LNG")).status).toBe(200);
});

test("refresh replaces the feed with a changed one", async () => {
    serve(makeArchive(), makeArchive(BOTH_WAYS));
    const planner = makePlanner();
    await getSchedule(planner, "LNG", "HSB");

    expect(await planner.refresh()).toBe(true);
    const schedule = await (await getSchedule(planner, "LNG", "HSB")).json<Schedule>();

    expect(schedule.sailings).toHaveLength(1);
    expect(schedule.notes).toEqual([]);
});

test("refresh asks for the feed only if it has changed", async () => {
    const fetch = serve({ body: makeArchive(), etag: '"first"' }, 304);
    const planner = makePlanner();

    expect(await planner.refresh()).toBe(true);
    expect(await planner.refresh()).toBe(false);

    expect(fetch).toHaveBeenLastCalledWith(GTFS_URL, { headers: { "If-None-Match": '"first"' } });
    expect((await getSchedule(planner, "HSB", "LNG")).status).toBe(200);
});

test("refresh keeps the feed when the server sends the same one again", async () => {
    // The second is not a feed, so reading it would fail.
    serve({ body: makeArchive(), etag: '"first"' }, { body: "unchanged", etag: '"first"' });
    const planner = makePlanner();
    await planner.refresh();

    expect(await planner.refresh()).toBe(false);
});

test("refresh remembers what it last downloaded when the planner restarts", async () => {
    const fetch = serve({ body: makeArchive(), etag: '"first"' });
    const planner = makePlanner();
    await planner.refresh();

    await evictDurableObject(planner);
    await planner.refresh();

    expect(fetch).toHaveBeenLastCalledWith(GTFS_URL, { headers: { "If-None-Match": '"first"' } });
});

test.each([
    ["cannot be downloaded", 503, "status 503"],
    ["is not a GTFS archive", "<html>Waiting room</html>", "invalid zip data"],
])("refresh fails and the previous feed is used when the feed %s", async (_, content, message) => {
    serve(makeArchive(), content);
    const planner = makePlanner();
    await planner.refresh();

    // Called from inside the planner, as an error that it throws to its caller is taken for one that nothing handles.
    await runInDurableObject(planner, async (instance) => {
        await expect(instance.refresh()).rejects.toThrow(message);
    });
    const schedule = await (await getSchedule(planner, "HSB", "LNG")).json<Schedule>();

    expect(schedule.sailings).toHaveLength(1);
});

test("route plans use the sailings from the feed", async () => {
    serve(makeArchive());

    const response = await post(makePlanner(), "/api/routeplans", {
        origin: "HSB",
        destination: "LNG",
        date: "2026-10-06",
    });

    expect(response.status).toBe(200);
    expect(await response.json()).toEqual([
        expect.objectContaining({
            // Check-in for booked vehicles closes 30 minutes before the sailing at 07:30, and the buffer is 15 minutes.
            depart_time: "2026-10-06T06:45:00",
            arrive_time: "2026-10-06T08:10:00",
            duration: 85 * 60,
        }),
    ]);
});

test("route plans leave more time before sailings when asked for a longer buffer", async () => {
    serve(makeArchive());

    const response = await post(makePlanner(), "/api/routeplans", {
        origin: "HSB",
        destination: "LNG",
        date: "2026-10-06",
        buffer: 30,
    });

    expect(await response.json()).toEqual([expect.objectContaining({ depart_time: "2026-10-06T06:30:00" })]);
});

test("no route plans when there is no feed", async () => {
    serve(503);

    const response = await post(makePlanner(), "/api/routeplans", { origin: "HSB", destination: "LNG" });

    expect(response.status).toBe(503);
    expect(await response.json()).toEqual({ detail: "Schedules are not available" });
});

test.each([
    ["is not JSON", "{", "request body must be a JSON object"],
    ["is not an object", [], "request body must be a JSON object"],
    ["has no origin", { destination: "LNG" }, "origin is not a known location"],
    ["has an unknown origin", { origin: "ATLANTIS", destination: "LNG" }, "origin is not a known location"],
    ["has an unknown destination", { origin: "HSB", destination: "toString" }, "destination is not a known location"],
    [
        "has the same origin and destination",
        { origin: "HSB", destination: "HSB" },
        "origin and destination cannot be the same",
    ],
    [
        "has a date that is not one",
        { origin: "HSB", destination: "LNG", date: "tomorrow" },
        "date is not a valid date",
    ],
    [
        "has a buffer that is not a number",
        { origin: "HSB", destination: "LNG", buffer: "long" },
        "buffer is not a number",
    ],
])("request is refused when it %s", async (_, body, detail) => {
    const fetch = serve(makeArchive());
    const planner = makePlanner();

    const response = await planner.fetch("https://planner/api/routeplans", {
        method: "POST",
        body: typeof body === "string" ? body : JSON.stringify(body),
    });

    expect(response.status).toBe(422);
    expect(await response.json()).toEqual({ detail });
    expect(fetch).not.toHaveBeenCalled();
});
