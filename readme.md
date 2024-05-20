# Ferry Planner

This website is a tool that calculates possible routes between two destinations with [BC Ferries](https://bcferries.com) sailings.

## Requirements

- [Python 3.11](https://www.python.org/downloads/) or higher
- Packages listed in [`requirements.txt`](requirements.txt)

## Development

To develop this project, install the required packages and run the server with the following commands:

```bash
pip install -e .
pip install -r requirements.txt -r requirements-dev.txt
uvicorn ferry_planner.server:app --reload
```

Navigate to <http://localhost:8000> to preview the website.

## Disclaimer

I am not liable for any data loss, damage, or any other consequences resulting from use of this software. Use at your own risk.

## License

[MIT License](license.txt)
