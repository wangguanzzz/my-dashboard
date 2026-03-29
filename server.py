#!/usr/bin/env python3
import base64
import http.server

USERNAME = "admin"
PASSWORD = "wangguanzhou"

class AuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Dashboard"')
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        if not self.authenticate():
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="Dashboard"')
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>401 Unauthorized</h1>")
            return
        super().do_GET()

    def authenticate(self):
        auth_header = self.headers.get("Authorization")
        if auth_header is None:
            return False
        try:
            auth_type, credentials = auth_header.split(" ", 1)
            if auth_type.lower() != "basic":
                return False
            decoded = base64.b64decode(credentials).decode("utf-8")
            user, passwd = decoded.split(":", 1)
            return user == USERNAME and passwd == PASSWORD
        except Exception:
            return False

    def log_message(self, format, *args):
        pass  # silence logs

if __name__ == "__main__":
    import os
    os.chdir("/home/ubuntu/.openclaw/workspace/dashboard")
    server = http.server.HTTPServer(("0.0.0.0", 80), AuthHandler)
    print("Dashboard running on port 80 with auth")
    server.serve_forever()
