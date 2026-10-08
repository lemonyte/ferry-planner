import { expect, test } from "vitest";
import schedules from "#test/fixtures/schedules.json";
import { makeTimetable } from "#test/fixtures.ts";
import type { TerminalId } from "./data/locations";
import { getSchedule } from "./schedule";
import { parseLocal } from "./time";

const timetable = makeTimetable();

test.each(schedules)(
    "schedule for $request.origin to $request.destination on $request.date is as expected",
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

test("schedule is for the day of the time it is asked for", () => {
    const schedule = getSchedule(timetable, "HSB", "NAN", parseLocal("2026-10-08T15:45:00") ?? Number.NaN);

    expect(schedule).toMatchObject({
        date: Date.UTC(2026, 9, 8, 15, 45),
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
