# Ferry Planner

This website is a tool that calculates possible routes between places with [BC Ferries](https://bcferries.com) sailings.

## How it works

The site is a [SvelteKit](https://svelte.dev/docs/kit) app that does its work in the browser:

- The browser downloads the BC Ferries [GTFS](https://gtfs.org) feed, reads it, and keeps it in local storage. It asks whether the feed has changed when the site is opened or come back to, at most once an hour.
- Routes are planned in the browser from that feed and the locations and connections in [`src/lib/planner/data/`](src/lib/planner/data).
- A service worker keeps the site itself, so it opens without a connection, and it can be installed as an app. Trips can be found offline once the feed has been downloaded.

The app is served by a [Cloudflare Worker](https://developers.cloudflare.com/workers/), which does nothing but pass the feed on at `/feed.zip`, as browsers are not let read it from the server that it is on.

## Development

You need [Bun](https://bun.sh).

```bash
bun install
bun run dev      # the website at http://localhost:5173
bun run test
bun run check    # check types, lint, and formatting
bun run build
bun run preview  # the built site as Cloudflare serves it, at http://localhost:4173
bun run deploy
```

The service worker only keeps files in the built site, so try the site offline with `bun run preview`.

The locations and connections are checked by the type checker and the tests, not when the site starts.
The expected results in [`test/fixtures/`](test/fixtures) are written by the planner itself. After a change that is meant to change them, write them again with `bun test/export-fixtures.ts` and look over what has changed.

## Disclaimer

I am not liable for any data loss, damage, or any other consequences resulting from use of this software. Use at your own risk.

## License

[MIT License](license.txt)
