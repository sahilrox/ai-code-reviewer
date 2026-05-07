import time
import jwt
import httpx
from backend.config import GITHUB_APP_ID, GITHUB_PRIVATE_KEY

def generate_jwt_token() -> str:
    """GitHub Apps authenticate using a short-lived JWT"""
    now = int(time.time())
    payload = {
        "iat": now - 60,
        "exp": now + (10 * 60),  # 10 minute expiry
        "iss": str(GITHUB_APP_ID)
    }
    return jwt.encode(payload, GITHUB_PRIVATE_KEY, algorithm="RS256")

async def get_installation_token(installation_id: int) -> str:
    """Exchange JWT for an installation access token"""
    jwt_token = generate_jwt_token()
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.github.com/app/installations/{installation_id}/access_tokens",
            headers={
                "Authorization": f"Bearer {jwt_token}",
                "Accept": "application/vnd.github+json"
            }
        )
        response.raise_for_status()
        return response.json()["token"]

async def get_pr_diff(repo_full_name: str, pr_number: int, token: str) -> str:
    """Fetch the raw diff of a PR"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3.diff"
            }
        )
        response.raise_for_status()
        return response.text

async def get_pr_details(repo_full_name: str, pr_number: int, token: str) -> dict:
    """Fetch PR metadata — title, author, latest commit SHA"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json"
            }
        )
        response.raise_for_status()
        data = response.json()
        return {
            "title": data["title"],
            "author": data["user"]["login"],
            "commit_sha": data["head"]["sha"]
        }

async def post_review(
    repo_full_name: str,
    pr_number: int,
    commit_sha: str,
    comments: list[dict],
    token: str
):
    """Post inline review comments back to the PR"""
    # Filter to only comments with valid line numbers
    valid_comments = [
        {
            "path": c["path"],
            "line": c["line"],
            "body": format_comment_body(c)
        }
        for c in comments
        if c.get("line") and c.get("path")
    ]

    summary = build_summary(comments)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}/reviews",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json"
            },
            json={
                "commit_id": commit_sha,
                "body": summary,
                "event": "COMMENT",
                "comments": valid_comments
            }
        )
        response.raise_for_status()
        return response.json()

def format_comment_body(comment: dict) -> str:
    icons = {"error": "🔴", "warning": "🟡", "suggestion": "🔵"}
    icon = icons.get(comment["severity"], "💬")
    return f"{icon} **{comment['severity'].upper()}**\n\n{comment['body']}"

def build_summary(comments: list[dict]) -> str:
    errors = sum(1 for c in comments if c["severity"] == "error")
    warnings = sum(1 for c in comments if c["severity"] == "warning")
    suggestions = sum(1 for c in comments if c["severity"] == "suggestion")
    return (
        f"## 🤖 AI Code Review\n\n"
        f"| 🔴 Errors | 🟡 Warnings | 🔵 Suggestions |\n"
        f"|-----------|-------------|----------------|\n"
        f"| {errors} | {warnings} | {suggestions} |\n\n"
        f"*Powered by Claude AI*"
    )