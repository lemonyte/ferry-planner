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

## Worker

The API is being moved to a [Cloudflare Worker](https://developers.cloudflare.com/workers/) in [`worker/`](worker), written in TypeScript and sized for the Workers Free plan.
The Worker answers `/api/locations` itself and passes `/api/routeplans` and `/api/ferry_schedule` to a single [Durable Object](https://developers.cloudflare.com/durable-objects/), which keeps the BC Ferries GTFS feed and plans routes with it.
The feed is checked for changes every hour.

You need [Bun](https://bun.sh) to work on it:

```bash
cd worker
bun install
bun run dev    # serve the API at http://localhost:8787
bun run test   # run the tests in the Workers runtime
bun run check  # check types, lint, and formatting
bun run deploy
```

The locations and connections in `worker/src/data/` are checked by the type checker and the tests, not when the Worker starts.
The expected results in `worker/test/fixtures/` come from the Python planner, and are made again with `uv run python tests/export_worker_fixtures.py`.

## Disclaimer

I am not liable for any data loss, damage, or any other consequences resulting from use of this software. Use at your own risk.

## License

[MIT License](license.txt)
