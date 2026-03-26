import asgi
from js import Response
from workers import Request, WorkerEntrypoint


class Default(WorkerEntrypoint):
    async def fetch(self, request: Request) -> Response:
        from ferry_planner.server import app

        return await asgi.fetch(app, request.js_object, self.env)
