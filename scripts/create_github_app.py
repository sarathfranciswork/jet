#!/usr/bin/env python3
"""
Create a GitHub App for Jet using the GitHub App Manifest flow.

This script:
1. Starts a temporary local HTTP server
2. Opens the browser with a form that submits the app manifest to GitHub
3. Handles the callback redirect to capture the code
4. Exchanges the code for app credentials via the GitHub API
5. Prints the credentials for configuration
"""

import http.server
import json
import os
import subprocess
import sys
import threading
import urllib.parse
import urllib.request

PORT = 3456
APP_URL = os.environ.get("JET_APP_URL", "http://34.55.60.88")
credentials = {}
server_should_stop = threading.Event()


MANIFEST = {
    "name": "jet-github-app",
    "url": APP_URL,
    "hook_attributes": {
        "url": f"{APP_URL}/api/webhooks/github/",
        "active": True,
    },
    "redirect_url": f"{APP_URL}/installations/github/",
    "callback_urls": [f"{APP_URL}/installations/github/"],
    "setup_url": f"{APP_URL}/installations/github/",
    "public": False,
    "default_permissions": {
        "issues": "write",
        "pull_requests": "write",
        "contents": "read",
        "metadata": "read",
    },
    "default_events": [
        "issues",
        "issue_comment",
        "pull_request",
        "pull_request_review",
        "label",
    ],
}


HTML_FORM = """<!DOCTYPE html>
<html>
<head><title>Creating Jet GitHub App...</title></head>
<body>
<h2>Creating GitHub App for Jet...</h2>
<p>You will be redirected to GitHub to confirm the app creation.</p>
<form id="manifest-form" method="post" action="https://github.com/settings/apps/new?state=jet-setup">
    <input type="hidden" name="manifest" value='{manifest_json}'>
    <button type="submit" style="padding:12px 24px; font-size:16px; cursor:pointer; background:#3B82F6; color:white; border:none; border-radius:6px;">
        Create GitHub App
    </button>
</form>
</body>
</html>"""


class CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/":
            # Serve the form page
            manifest_json = json.dumps(MANIFEST).replace("'", "&#39;")
            html = HTML_FORM.replace("{manifest_json}", manifest_json)
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())

        elif parsed.path == "/callback":
            # Handle the redirect from GitHub with the code
            params = urllib.parse.parse_qs(parsed.query)
            code = params.get("code", [None])[0]

            if code:
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(
                    b"<html><body><h2>GitHub App created! Exchanging code for credentials...</h2></body></html>"
                )
                # Exchange code for credentials
                exchange_code(code)
            else:
                self.send_response(400)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(b"<html><body><h2>Error: No code received</h2></body></html>")

            server_should_stop.set()
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Suppress log output


def exchange_code(code):
    """Exchange the manifest code for app credentials."""
    global credentials
    url = f"https://api.github.com/app-manifests/{code}/conversions"
    req = urllib.request.Request(
        url,
        method="POST",
        headers={
            "Accept": "application/vnd.github+json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            credentials = json.loads(resp.read().decode())
            print("\n" + "=" * 60)
            print("  GITHUB APP CREATED SUCCESSFULLY!")
            print("=" * 60)
            print(f"\n  App Name:        {credentials.get('name', 'N/A')}")
            print(f"  App ID:          {credentials.get('id', 'N/A')}")
            print(f"  App Slug:        {credentials.get('slug', 'N/A')}")
            print(f"  Client ID:       {credentials.get('client_id', 'N/A')}")
            print(f"  Client Secret:   {credentials.get('client_secret', 'N/A')}")
            print(f"  Webhook Secret:  {credentials.get('webhook_secret', 'N/A')}")
            print(f"  HTML URL:        {credentials.get('html_url', 'N/A')}")
            print(f"\n  Private Key (PEM):")
            pem = credentials.get("pem", "")
            print(f"  {pem[:80]}...")
            print("=" * 60)

            # Save credentials to a file
            creds_file = os.path.join(os.path.dirname(__file__), "github_app_credentials.json")
            with open(creds_file, "w") as f:
                json.dump(credentials, f, indent=2)
            print(f"\n  Full credentials saved to: {creds_file}")
            print("=" * 60 + "\n")

    except Exception as e:
        print(f"\nError exchanging code: {e}")


def main():
    # Update manifest redirect to local callback
    MANIFEST["redirect_url"] = f"http://localhost:{PORT}/callback"

    server = http.server.HTTPServer(("", PORT), CallbackHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    print(f"\nLocal server started on http://localhost:{PORT}")
    print(f"Opening browser to create GitHub App...\n")

    # Open browser
    subprocess.run(["open", f"http://localhost:{PORT}"], check=False)

    # Wait for callback or timeout
    server_should_stop.wait(timeout=300)  # 5 minute timeout
    server.shutdown()

    if credentials:
        print("Done! Use the credentials above to configure the deployment.")
    else:
        print("Timed out or failed. Please try again.")


if __name__ == "__main__":
    main()
