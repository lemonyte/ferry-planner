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

## Disclaimer

I am not liable for any data loss, damage, or any other consequences resulting from use of this software. Use at your own risk.

## License

[MIT License](license.txt)
