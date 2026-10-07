import { locations } from "./data/locations";

export { Planner } from "./planner";

const PLANNER_ROUTES = ["/api/routeplans", "/api/ferry_schedule"];

const getPlanner = (env: Env) => {
    return env.PLANNER.getByName("bcferries", { locationHint: "wnam" });
};

export default {
    // Almost all the work is left to the planner, which gets more CPU time than a Worker does on the Workers Free plan.
    async fetch(request, env): Promise<Response> {
        const { pathname } = new URL(request.url);
        const method = PLANNER_ROUTES.includes(pathname) ? "POST" : pathname === "/api/locations" ? "GET" : undefined;
        if (!method) {
            return Response.json({ detail: "Not Found" }, { status: 404 });
        }
        if (request.method !== method) {
            return Response.json({ detail: "Method Not Allowed" }, { status: 405, headers: { Allow: method } });
        }
        if (method === "GET") {
            return Response.json(locations, { headers: { "Cache-Control": "public, max-age=3600" } });
        }
        return getPlanner(env).fetch(request);
    },

    async scheduled(_controller, env): Promise<void> {
        await getPlanner(env).refresh();
    },
} satisfies ExportedHandler<Env>;
