import { createHash } from "node:crypto";

const sortKeys = (value: unknown): unknown => {
    if (Array.isArray(value)) {
        return value.map(sortKeys);
    }
    if (value && typeof value === "object") {
        return Object.fromEntries(
            Object.entries(value)
                .filter(([, item]) => item !== undefined)
                .sort(([a], [b]) => (a < b ? -1 : 1))
                .map(([key, item]) => [key, sortKeys(item)]),
        );
    }
    return value;
};

/** Hash a value whatever order its keys are in, to keep in place of a result too long to keep whole. */
export const digest = (value: unknown): string => {
    return createHash("sha256")
        .update(JSON.stringify(sortKeys(value)))
        .digest("hex");
};
