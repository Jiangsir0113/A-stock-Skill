# URL MCP Guide

Use this guide when the user provides requirement URLs and the skill should access them through MCP.

## Core Rule

When the user gives a URL, prefer the built-in MCP URL reader instead of treating the link as plain text.

## Built-In MCP Server

This skill bundles a local MCP server script:

- `scripts/url_reader_mcp.py`

Default endpoint:

- `http://127.0.0.1:8765/mcp`

Health check:

- `http://127.0.0.1:8765/health`

## Startup

Start it with:

```bash
python3 scripts/url_reader_mcp.py
```

Or use the helper script:

```bash
bash scripts/start_url_reader_mcp.sh
```

Optional environment variables:

- `JAVA_URL_MCP_HOST`
- `JAVA_URL_MCP_PORT`
- `JAVA_URL_MCP_PATH`

## Tool Provided

The MCP server exposes one tool:

- `fetch_url`

Arguments:

- `url` required
- `timeout_seconds` optional
- `max_chars` optional
- `headers` optional
- `cookies` optional

## When To Use It

Use this MCP when the user provides:

- PRD URLs
- prototype URLs
- Lanhu links
- any other requirement page URL

If the URL requires login or special access, ask the user for:

- required headers
- cookies
- other access context needed to read the page

## Expected Behavior

The URL reader fetches the page, converts HTML to readable text when needed, and returns the content for requirement analysis.

It also:

- follows redirects
- returns the final URL and HTTP status
- ignores common HTML noise such as script and style blocks

If the MCP server is not running, tell the user the local URL reader MCP needs to be started first.
