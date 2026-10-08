import { expect, test } from "vitest";
import schedules from "#test/fixtures/schedules.json";
import { makeTimetable } from "#test/fixtures.ts";
import type { TerminalId } from "./data/locations";
import { getSchedule, scheduleResponse } from "./schedule";
import { parseLocal } from "./time";

const timetable = makeTimetable();

test.each(schedules)(
    "schedule for $request.origin to $request.destination on $request.date is the same as from the Python planner",
    ({ request, response }) => {
        const schedule = getSchedule(
            timetable,
            request.origin as TerminalId,
            request.destination as TerminalId,
            parseLocal(request.date) ?? Number.NaN,
        );

        expect(scheduleResponse(schedule)).toEqual(response);
    },
);

test("schedule is for the day of the time it is asked for", () => {
    const schedule = getSchedule(timetable, "HSB", "NAN", parseLocal("2026-10-08T15:45:00") ?? Number.NaN);

    expect(scheduleResponse(schedule)).toMatchObject({
        date: "2026-10-08T15:45:00",
        sailings: expect.objectContaining({ length: 7 }),
        url: "https://www.bcferries.com/routes-fares/schedules/daily/HSB-NAN?&scheduleDate=10/08/2026",
    });
});

test("no sailings between terminals that are only joined by way of another, where the vessel is changed", () => {
    const date = parseLocal("2026-10-08") ?? Number.NaN;

    expect(getSchedule(timetable, "CMX", "TEX", date)).toMatchObject({ sailings: [], notes: ["No sailings found"] });
    expect(getSchedule(timetable, "CMX", "PWR", date).sailings).toHaveLength(4);
    expect(getSchedule(timetable, "PWR", "TEX", date).sailings).toHaveLength(8);
});

test("sailing that calls at terminals on its way is between the first and the last of them", () => {
    const schedule = getSchedule(timetable, "TSA", "PLH", parseLocal("2026-10-08") ?? Number.NaN);

    expect(scheduleResponse(schedule).sailings).toEqual([
        {
            departure: "2026-10-08T10:25:00-07:00",
            arrival: "2026-10-08T13:20:00-07:00",
            duration: 175 * 60,
            notes: ["Via Sturdies Bay Terminal, Village Bay Terminal, Otter Bay Terminal"],
        },
        {
            departure: "2026-10-08T19:30:00-07:00",
            arrival: "2026-10-08T22:30:00-07:00",
            duration: 180 * 60,
            notes: ["Via Sturdies Bay Terminal, Village Bay Terminal, Otter Bay Terminal"],
        },
    ]);
});
