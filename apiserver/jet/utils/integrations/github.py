import os
import hashlib
import hmac
import jwt
import logging
import requests
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend
from django.conf import settings

logger = logging.getLogger(__name__)


def _get_private_key_bytes():
    """Load the GitHub App private key from env var or file."""
    import base64

    # Try base64-encoded env var first
    b64_key = os.environ.get("GITHUB_APP_PRIVATE_KEY_BASE64", "")
    if b64_key:
        return base64.b64decode(b64_key)

    # Try raw PEM env var (with literal \n replaced)
    raw_key = os.environ.get("GITHUB_APP_PRIVATE_KEY", "")
    if raw_key:
        # Handle env vars where newlines are stored as literal \n
        raw_key = raw_key.replace("\\n", "\n")
        return raw_key.encode("utf8")

    # Try PEM file path
    pem_path = os.environ.get(
        "GITHUB_APP_PRIVATE_KEY_PATH",
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "github_app_key.pem"),
    )
    if os.path.exists(pem_path):
        with open(pem_path, "rb") as f:
            return f.read()

    return b""


def get_jwt_token():
    app_id = os.environ.get("GITHUB_APP_ID", "")
    secret = _get_private_key_bytes()
    current_timestamp = int(datetime.now().timestamp())
    due_date = datetime.now() + timedelta(minutes=10)
    expiry = int(due_date.timestamp())
    payload = {
        "iss": app_id,
        "sub": app_id,
        "exp": expiry,
        "iat": current_timestamp,
        "aud": "https://github.com/login/oauth/access_token",
    }

    priv_rsakey = load_pem_private_key(secret, None, default_backend())
    token = jwt.encode(payload, priv_rsakey, algorithm="RS256")
    return token


def get_github_metadata(installation_id):
    token = get_jwt_token()

    url = f"https://api.github.com/app/installations/{installation_id}"
    headers = {
        "Authorization": "Bearer " + str(token),
        "Accept": "application/vnd.github+json",
    }
    response = requests.get(url, headers=headers).json()
    return response


def get_github_repos(access_tokens_url, repositories_url):
    token = get_jwt_token()

    headers = {
        "Authorization": "Bearer " + str(token),
        "Accept": "application/vnd.github+json",
    }

    oauth_response = requests.post(
        access_tokens_url,
        headers=headers,
    ).json()

    oauth_token = oauth_response.get("token", "")
    headers = {
        "Authorization": "Bearer " + str(oauth_token),
        "Accept": "application/vnd.github+json",
    }
    response = requests.get(
        repositories_url,
        headers=headers,
    ).json()
    return response


def delete_github_installation(installation_id):
    token = get_jwt_token()

    url = f"https://api.github.com/app/installations/{installation_id}"
    headers = {
        "Authorization": "Bearer " + str(token),
        "Accept": "application/vnd.github+json",
    }
    response = requests.delete(url, headers=headers)
    return response


def get_github_repo_details(access_tokens_url, owner, repo):
    token = get_jwt_token()

    headers = {
        "Authorization": "Bearer " + str(token),
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    oauth_response = requests.post(
        access_tokens_url,
        headers=headers,
    ).json()

    oauth_token = oauth_response.get("token")
    headers = {
        "Authorization": "Bearer " + oauth_token,
        "Accept": "application/vnd.github+json",
    }
    open_issues = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}",
        headers=headers,
    ).json()["open_issues_count"]

    total_labels = 0

    labels_response = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/labels?per_page=100&page=1",
        headers=headers,
    )

    # Check if there are more pages
    if len(labels_response.links.keys()):
        # get the query parameter of last
        last_url = labels_response.links.get("last").get("url")
        parsed_url = urlparse(last_url)
        last_page_value = parse_qs(parsed_url.query)["page"][0]
        total_labels = total_labels + 100 * (int(last_page_value) - 1)

        # Get labels in last page
        last_page_labels = requests.get(last_url, headers=headers).json()
        total_labels = total_labels + len(last_page_labels)
    else:
        total_labels = len(labels_response.json())

    # Currently only supporting upto 100 collaborators
    # TODO: Update this function to fetch all collaborators
    collaborators = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/collaborators?per_page=100&page=1",
        headers=headers,
    ).json()

    return open_issues, total_labels, collaborators


def get_release_notes():
    token = settings.GITHUB_ACCESS_TOKEN

    if token:
        headers = {
            "Authorization": "Bearer " + str(token),
            "Accept": "application/vnd.github.v3+json",
        }
    else:
        headers = {
            "Accept": "application/vnd.github.v3+json",
        }
    url = "https://api.github.com/repos/makeplane/jet/releases?per_page=5&page=1"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": "Unable to render information from Github Repository"}

    return response.json()


def verify_github_webhook_signature(payload_body, signature_header, secret):
    """Verify that the webhook payload was sent from GitHub by validating SHA256."""
    if not signature_header:
        return False
    hash_object = hmac.new(
        secret.encode("utf-8"), msg=payload_body, digestmod=hashlib.sha256
    )
    expected_signature = "sha256=" + hash_object.hexdigest()
    return hmac.compare_digest(expected_signature, signature_header)


class GithubAPIClient:
    """Client for interacting with the GitHub API using installation tokens."""

    BASE_URL = "https://api.github.com"

    def __init__(self, access_tokens_url):
        self.access_tokens_url = access_tokens_url
        self._token = None
        self._token_expires_at = None

    def _get_installation_token(self):
        """Get or refresh installation access token."""
        now = datetime.now()
        if self._token and self._token_expires_at and now < self._token_expires_at:
            return self._token

        jwt_token = get_jwt_token()
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/vnd.github+json",
        }
        response = requests.post(self.access_tokens_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        self._token = data.get("token")
        expires_at = data.get("expires_at")
        if expires_at:
            self._token_expires_at = datetime.fromisoformat(
                expires_at.replace("Z", "+00:00")
            ).replace(tzinfo=None) - timedelta(minutes=1)
        else:
            self._token_expires_at = now + timedelta(minutes=55)
        return self._token

    def _headers(self):
        token = self._get_installation_token()
        return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def _request(self, method, path, **kwargs):
        url = f"{self.BASE_URL}{path}"
        response = requests.request(method, url, headers=self._headers(), **kwargs)
        response.raise_for_status()
        if response.status_code == 204:
            return None
        return response.json()

    # --- Issues ---
    def get_issue(self, owner, repo, issue_number):
        return self._request("GET", f"/repos/{owner}/{repo}/issues/{issue_number}")

    def create_issue(self, owner, repo, title, body=None, labels=None, assignees=None):
        data = {"title": title}
        if body:
            data["body"] = body
        if labels:
            data["labels"] = labels
        if assignees:
            data["assignees"] = assignees
        return self._request("POST", f"/repos/{owner}/{repo}/issues", json=data)

    def update_issue(self, owner, repo, issue_number, **kwargs):
        data = {}
        for key in ("title", "body", "state", "labels", "assignees"):
            if key in kwargs:
                data[key] = kwargs[key]
        return self._request(
            "PATCH", f"/repos/{owner}/{repo}/issues/{issue_number}", json=data
        )

    def close_issue(self, owner, repo, issue_number):
        return self.update_issue(owner, repo, issue_number, state="closed")

    def reopen_issue(self, owner, repo, issue_number):
        return self.update_issue(owner, repo, issue_number, state="open")

    # --- Comments ---
    def create_comment(self, owner, repo, issue_number, body):
        return self._request(
            "POST",
            f"/repos/{owner}/{repo}/issues/{issue_number}/comments",
            json={"body": body},
        )

    def update_comment(self, owner, repo, comment_id, body):
        return self._request(
            "PATCH",
            f"/repos/{owner}/{repo}/issues/comments/{comment_id}",
            json={"body": body},
        )

    def delete_comment(self, owner, repo, comment_id):
        return self._request(
            "DELETE", f"/repos/{owner}/{repo}/issues/comments/{comment_id}"
        )

    # --- Labels ---
    def create_label(self, owner, repo, name, color=None, description=None):
        data = {"name": name}
        if color:
            data["color"] = color.lstrip("#")
        if description:
            data["description"] = description
        return self._request("POST", f"/repos/{owner}/{repo}/labels", json=data)

    def list_labels(self, owner, repo, per_page=100):
        return self._request(
            "GET", f"/repos/{owner}/{repo}/labels?per_page={per_page}"
        )

    # --- Pull Requests ---
    def get_pull_request(self, owner, repo, pr_number):
        return self._request("GET", f"/repos/{owner}/{repo}/pulls/{pr_number}")

    # --- Webhooks ---
    def register_webhook(self, owner, repo, webhook_url, secret, events=None):
        if events is None:
            events = [
                "issues",
                "issue_comment",
                "pull_request",
                "pull_request_review",
                "label",
            ]
        data = {
            "name": "web",
            "active": True,
            "events": events,
            "config": {
                "url": webhook_url,
                "content_type": "json",
                "secret": secret,
                "insecure_ssl": "0",
            },
        }
        return self._request("POST", f"/repos/{owner}/{repo}/hooks", json=data)
