import asgi
from js import Response
from workers import Request, WorkerEntrypoint

from ferry_planner.server import app


class Default(WorkerEntrypoint):
    async def fetch(self, request: Request) -> Response:
        return await asgi.fetch(app, request.js_object, self.env)
