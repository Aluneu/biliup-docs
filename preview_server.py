#!/usr/bin/env python3
# Minimal static server for the built VitePress site (dist/).
# Handles the site base "/biliup-docs/" by mapping /biliup-docs/* -> dist/*.
import http.server
import os
import socketserver
from urllib.parse import urlparse, unquote

DIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs", ".vitepress", "dist")
BASE = "/biliup-docs"
PORT = int(os.environ.get("PORT", 8092))

CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".ico": "image/x-icon",
    ".woff2": "font/woff2",
    ".woff": "font/woff",
}


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIST, **kwargs)

    def translate_path(self, path):
        parsed = urlparse(path)
        p = unquote(parsed.path)
        if p == "/" or p == "":
            p = BASE + "/"
        if p.startswith(BASE + "/"):
            p = p[len(BASE) + 1:]
            if p == "":
                p = "index.html"
        # default file for directory-like paths
        candidate = os.path.normpath(os.path.join(DIST, p.lstrip("/")))
        if os.path.isdir(candidate):
            candidate = os.path.join(candidate, "index.html")
        return candidate

    def do_GET(self):
        target = self.translate_path(self.path)
        if os.path.isfile(target):
            ext = os.path.splitext(target)[1].lower()
            self.send_response(200)
            self.send_header("Content-Type", CONTENT_TYPES.get(ext, "application/octet-stream"))
            self.send_header("Content-Length", str(os.path.getsize(target)))
            self.end_headers()
            with open(target, "rb") as f:
                self.wfile.write(f.read())
        else:
            # SPA-ish fallback: try .html sibling
            alt = target
            if not alt.endswith(".html"):
                alt = target + ".html"
            if os.path.isfile(alt):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(alt, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "Not Found: " + self.path)


if __name__ == "__main__":
    os.chdir(DIST)
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"Serving {DIST}")
        print(f"Open: http://localhost:{PORT}{BASE}/")
        httpd.serve_forever()
