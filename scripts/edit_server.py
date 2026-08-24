#!/usr/bin/env python3
"""
Local preview server with in-page WYSIWYG editing.

Usage:
    python3 scripts/edit_server.py [port]      # default port 8765

Then open http://127.0.0.1:8765/ — every HTML page gets a small
"Edit page" toolbar (bottom right). Click it, edit text directly on the
page, then "Save": the server rewrites the corresponding .html file on
disk. Files are only ever overwritten, never created, and the repo is
under git, so any save can be reverted.

Notes:
  - Responses are served with no-store caching, so edits always show up
    on refresh (no more ?v= cache busting while previewing).
  - The editor script (scripts/editor.js) is injected before </body> at
    serve time only; it strips itself out again before saving.
"""
import http.server
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDITOR_JS = os.path.join(ROOT, "scripts", "editor.js")
INJECT = b'<script src="/_editor.js" data-vl-editor></script>\n</body>'


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    # ------------------------------------------------------------------ GET
    def do_GET(self):
        clean = self.path.split("?", 1)[0].split("#", 1)[0]
        if clean == "/_editor.js":
            return self._serve_bytes(open(EDITOR_JS, "rb").read(), "text/javascript")
        target = self._resolve(clean)
        if target and target.endswith(".html") and os.path.isfile(target):
            page = open(target, "rb").read()
            if b"</body>" in page:
                page = page.replace(b"</body>", INJECT, 1)
            return self._serve_bytes(page, "text/html; charset=utf-8")
        return super().do_GET()

    # ----------------------------------------------------------------- POST
    def do_POST(self):
        if self.path.split("?", 1)[0] != "/_save":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length).decode("utf-8"))
            target = self._resolve(data["path"].split("?", 1)[0])
            html = data["html"]
        except Exception as exc:  # malformed request
            return self._respond(400, {"ok": False, "error": str(exc)})

        if not target or not target.endswith(".html"):
            return self._respond(400, {"ok": False, "error": "not an html path"})
        if not os.path.isfile(target):
            return self._respond(403, {"ok": False, "error": "refusing to create new files"})
        if "<body" not in html or "</html>" not in html:
            return self._respond(400, {"ok": False, "error": "payload does not look like a full page"})

        with open(target, "w", encoding="utf-8") as f:
            f.write(html)
        rel = os.path.relpath(target, ROOT)
        print(f"  saved {rel} ({len(html)} chars)")
        return self._respond(200, {"ok": True, "file": rel})

    # -------------------------------------------------------------- helpers
    def _resolve(self, urlpath):
        """Map a URL path to a real file under ROOT (dirs -> index.html)."""
        path = self.translate_path(urlpath)
        if os.path.isdir(path):
            path = os.path.join(path, "index.html")
        real = os.path.realpath(path)
        if real != os.path.realpath(ROOT) and not real.startswith(os.path.realpath(ROOT) + os.sep):
            return None
        return real

    def _serve_bytes(self, body, ctype):
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _respond(self, code, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Editing preview at http://127.0.0.1:{port}/  (Ctrl-C to stop)")
    server.serve_forever()


if __name__ == "__main__":
    main()
