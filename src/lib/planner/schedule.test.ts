import { expect, test } from "vitest";

import { makeTimetable } from "#test/fixtures.ts";
import schedules from "#test/fixtures/schedules.json";

import type { TerminalId } from "./data/locations.ts";
import { getSchedule } from "./schedule.ts";
import { parseLocal } from "./time.ts";

const timetable = makeTimetable();

test.each(schedules)(
    "getSchedule returns the expected schedule for $request.origin to $request.destination on $request.date",
    ({ request, response }) => {
        const schedule = getSchedule(
            timetable,
            request.origin as TerminalId,
            request.destination as TerminalId,
            parseLocal(request.date) ?? Number.NaN,
        );

        expect(schedule).toEqual(response);
    },
);

test("getSchedule uses the day of the given time", () => {
    const schedule = getSchedule(timetable, "HSB", "NAN", parseLocal("2026-10-08T15:45:00") ?? Number.NaN);

    expect(schedule).toMatchObject({
        sailings: expect.objectContaining({ length: 7 }),
        url: "https://www.bcferries.com/routes-fares/schedules/daily/HSB-NAN?&scheduleDate=10/08/2026",
    });
});

test("getSchedule returns no sailings between terminals that are connected only by changing vessels", () => {
    const date = parseLocal("2026-10-08") ?? Number.NaN;

    expect(getSchedule(timetable, "CMX", "TEX", date)).toMatchObject({ sailings: [] });
    expect(getSchedule(timetable, "CMX", "PWR", date).sailings).toHaveLength(4);
    expect(getSchedule(timetable, "PWR", "TEX", date).sailings).toHaveLength(8);
});

test("multi-stop sailing runs from its first terminal to its last", () => {
    const schedule = getSchedule(timetable, "TSA", "PLH", parseLocal("2026-10-08") ?? Number.NaN);

    expect(schedule.sailings).toEqual([
        {
            departure: Date.UTC(2026, 9, 8, 10, 25),
            arrival: Date.UTC(2026, 9, 8, 13, 20),
            stops: ["PSB", "PVB", "POB"],
        },
        {
            departure: Date.UTC(2026, 9, 8, 19, 30),
            arrival: Date.UTC(2026, 9, 8, 22, 30),
            stops: ["PSB", "PVB", "POB"],
        },
    ]);
});
