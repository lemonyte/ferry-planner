# Ferry Planner

This website is a tool that calculates possible routes between places with [BC Ferries](https://bcferries.com) sailings.

## Requirements

- [Python 3.11](https://www.python.org/downloads/) or higher

## Development

To develop this project, install the required packages and run the server with the following commands:

```bash
pip install -e .
uvicorn ferry_planner.server:app --reload
```

### Building CSS output

You need to build the CSS file with [Tailwind](https://tailwindcss.com/docs/installation/tailwind-cli) before running the server for the first time:

```bash
npx @tailwindcss/cli -i ./src/ferry_planner/static/style-in.css -o ./src/ferry_planner/static/style-out.css
```

Navigate to <http://localhost:8000> to preview the website.

## Workers

The site is being moved to [Cloudflare Workers](https://developers.cloudflare.com/workers/), sized for the Workers Free plan. There are two, each a project of its own that needs [Bun](https://bun.sh):

- [`worker/`](worker) is the backend, written in TypeScript. It answers `/api/locations` itself and passes the rest of `/api/*` to a single [Durable Object](https://developers.cloudflare.com/durable-objects/), which keeps the BC Ferries GTFS feed and plans routes with it. The feed is checked for changes every hour.
- [`web/`](web) is the website, a [SvelteKit](https://svelte.dev/docs/kit) app rendered on the server. It asks the backend for the routes worth taking through a service binding, at `/api/search`.

```bash
cd worker       # or web
bun install
bun run dev     # the backend at http://localhost:8787, the website at http://localhost:5173
bun run test
bun run check   # check types, lint, and formatting
bun run deploy
```

The website needs the backend running beside it. Deploy the backend first when both have changed.

The locations and connections in `worker/src/data/` are checked by the type checker and the tests, not when the Worker starts.
The expected results in `worker/test/fixtures/` come from the Python planner, and are made again with `uv run python tests/export_worker_fixtures.py`.

## Disclaimer

I am not liable for any data loss, damage, or any other consequences resulting from use of this software. Use at your own risk.

## License

[MIT License](license.txt)
