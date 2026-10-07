import { expect, test } from "vitest";
import type { TerminalId } from "../src/data/locations";
import { getSchedule, scheduleResponse } from "../src/schedule";
import { parseLocal } from "../src/time";
import { makeTimetable } from "./fixtures";
import schedules from "./fixtures/schedules.json";

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
