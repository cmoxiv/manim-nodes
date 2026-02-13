"""
Tiny host-side helper that opens local folders in Finder.
Run this on the host alongside docker-compose so the "open folder"
buttons work when the backend is running in Docker.

Usage: python scripts/folder-opener.py
"""
import subprocess
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

PORT = 8001


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length else {}
        path = body.get("path", "")

        if not path:
            self._respond(400, {"error": "missing path"})
            return

        if sys.platform == "darwin":
            subprocess.Popen(["open", path])
        elif sys.platform == "win32":
            subprocess.Popen(["explorer", path])
        else:
            subprocess.Popen(["xdg-open", path])

        self._respond(200, {"ok": True})

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _respond(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        print(f"[folder-opener] {args[0]}")


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Folder opener listening on http://127.0.0.1:{PORT}")
    server.serve_forever()
