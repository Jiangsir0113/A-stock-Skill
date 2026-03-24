#!/usr/bin/env python3
"""
Minimal local MCP server for reading URLs.

Run:
    python3 scripts/url_reader_mcp.py

Then expose the MCP endpoint at:
    http://127.0.0.1:8765/mcp
"""

from __future__ import annotations

import json
import os
import re
import socketserver
import sys
from http import cookies
import urllib.error
import urllib.request
from html.parser import HTMLParser
from http.server import BaseHTTPRequestHandler


HOST = os.environ.get("JAVA_URL_MCP_HOST", "127.0.0.1")
PORT = int(os.environ.get("JAVA_URL_MCP_PORT", "8765"))
PATH = os.environ.get("JAVA_URL_MCP_PATH", "/mcp")
USER_AGENT = "java-architect-assistant-url-reader/1.0"
OAUTH_METADATA = {
    "issuer": f"http://{HOST}:{PORT}",
    "authorization_endpoint": None,
    "token_endpoint": None,
    "response_types_supported": [],
    "grant_types_supported": [],
    "token_endpoint_auth_methods_supported": [],
}


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip_tags = {"script", "style", "noscript", "svg"}
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del attrs
        if tag.lower() in self.skip_tags:
            self.skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in self.skip_tags and self.skip_depth > 0:
            self.skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.skip_depth > 0:
            return
        stripped = data.strip()
        if stripped:
            self.parts.append(stripped)

    def text(self) -> str:
        return "\n".join(self.parts)


def normalize_text(text: str, max_chars: int) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if len(text) > max_chars:
        return text[:max_chars] + "\n\n[truncated]"
    return text


def build_cookie_header(cookie_value: object) -> str:
    if isinstance(cookie_value, str):
        return cookie_value.strip()
    if isinstance(cookie_value, dict):
        jar = cookies.SimpleCookie()
        for key, value in cookie_value.items():
            jar[str(key)] = str(value)
        return "; ".join(m.OutputString() for m in jar.values())
    raise ValueError("cookies must be a string or object")


def build_headers(args: dict) -> dict[str, str]:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }

    extra_headers = args.get("headers", {})
    if extra_headers:
        if not isinstance(extra_headers, dict):
            raise ValueError("headers must be an object")
        for key, value in extra_headers.items():
            headers[str(key)] = str(value)

    cookie_value = args.get("cookies")
    if cookie_value:
        headers["Cookie"] = build_cookie_header(cookie_value)

    return headers


def fetch_url(args: dict) -> dict:
    url = args.get("url", "").strip()
    timeout = int(args.get("timeout_seconds", 20))
    max_chars = int(args.get("max_chars", 20000))
    headers = build_headers(args)

    if not url:
        raise ValueError("Missing required argument: url")
    if not re.match(r"^https?://", url, re.IGNORECASE):
        raise ValueError("Only http:// or https:// URLs are supported")
    if timeout <= 0:
        raise ValueError("timeout_seconds must be positive")
    if max_chars <= 0:
        raise ValueError("max_chars must be positive")

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            final_url = resp.geturl()
            status = getattr(resp, "status", 200)
            content_type = resp.headers.get("Content-Type", "")
            charset = resp.headers.get_content_charset() or "utf-8"
            text = raw.decode(charset, errors="replace")
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Failed to fetch URL: {exc}") from exc

    if "html" in content_type.lower():
        parser = TextExtractor()
        parser.feed(text)
        text = parser.text()

    text = normalize_text(text, max_chars=max_chars)
    return {
        "content": [
            {
                "type": "text",
                "text": (
                    f"URL: {url}\n"
                    f"Final-URL: {final_url}\n"
                    f"Status: {status}\n"
                    f"Content-Type: {content_type or 'unknown'}\n\n{text}"
                ),
            }
        ]
    }


TOOLS = [
    {
        "name": "fetch_url",
        "description": "Fetch a URL and return readable text content for requirement analysis.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The http or https URL to fetch.",
                },
                "timeout_seconds": {
                    "type": "integer",
                    "description": "Optional timeout in seconds. Default is 20.",
                },
                "max_chars": {
                    "type": "integer",
                    "description": "Optional output length cap. Default is 20000.",
                },
                "headers": {
                    "type": "object",
                    "description": "Optional request headers, useful for authenticated or protected pages.",
                    "additionalProperties": {"type": "string"},
                },
                "cookies": {
                    "description": "Optional cookie header value as a string, or a cookie object map.",
                    "oneOf": [
                        {"type": "string"},
                        {
                            "type": "object",
                            "additionalProperties": {"type": "string"},
                        },
                    ],
                },
            },
            "required": ["url"],
        },
    }
]


def handle_rpc(payload: dict) -> tuple[int, dict | None]:
    method = payload.get("method")
    request_id = payload.get("id")

    if method == "initialize":
        return 200, {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {
                    "name": "java-url-reader-mcp",
                    "version": "1.0.0",
                },
            },
        }

    if method == "notifications/initialized":
        return 204, None

    if method == "tools/list":
        return 200, {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"tools": TOOLS},
        }

    if method == "tools/call":
        params = payload.get("params", {})
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        if tool_name != "fetch_url":
            return 200, {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32602,
                    "message": f"Unknown tool: {tool_name}",
                },
            }
        try:
            result = fetch_url(arguments)
        except Exception as exc:  # noqa: BLE001
            return 200, {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32000,
                    "message": str(exc),
                },
            }
        return 200, {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result,
        }

    return 200, {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


class ThreadingHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if self.path in {
            "/.well-known/oauth-authorization-server",
            "/.well-known/oauth-authorization-server/mcp",
            f"{PATH}/.well-known/oauth-authorization-server",
        }:
            encoded = json.dumps(OAUTH_METADATA).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)
            return
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"ok")
            return
        self.send_response(404)
        self.end_headers()

    def do_POST(self) -> None:  # noqa: N802
        if self.path != PATH:
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            return

        status, body = handle_rpc(payload)
        self.send_response(status)
        if body is not None:
            encoded = json.dumps(body).encode("utf-8")
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)
            return
        self.end_headers()

    def log_message(self, fmt: str, *args: object) -> None:
        sys.stderr.write(fmt % args)
        sys.stderr.write("\n")


def main() -> None:
    with ThreadingHTTPServer((HOST, PORT), Handler) as server:
        print(f"java-url-reader-mcp listening on http://{HOST}:{PORT}{PATH}")
        server.serve_forever()


if __name__ == "__main__":
    main()
