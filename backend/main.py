import hmac
import hashlib
import json
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.config import GITHUB_WEBHOOK_SECRET
from backend.github_client import (
    get_installation_token,
    get_pr_diff,
    get_pr_details,
    post_review
)
from backend.llm_reviewer import review_diff
from backend.db import save_review, get_recent_reviews

app = FastAPI(title="AI Code Reviewer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)

def verify_signature(payload: bytes, signature: str) -> bool:
    expected = "sha256=" + hmac.new(
        GITHUB_WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)

@app.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.body()
    sig = request.headers.get("X-Hub-Signature-256", "")

    if not verify_signature(payload, sig):
        raise HTTPException(status_code=401, detail="Invalid signature")

    event = request.headers.get("X-GitHub-Event")
    data = json.loads(payload)

    if event == "pull_request" and data["action"] in ["opened", "synchronize"]:
        repo = data["repository"]["full_name"]
        pr_number = data["pull_request"]["number"]
        installation_id = data["installation"]["id"]

        print(f"✅ PR event received: {repo} #{pr_number}")

        try:
            # Step 1: Auth with GitHub
            token = await get_installation_token(installation_id)
            print(f"✅ Got installation token")

            # Step 2: Fetch PR info
            details = await get_pr_details(repo, pr_number, token)
            print(f"✅ PR details: {details}")

            diff = await get_pr_diff(repo, pr_number, token)
            print(f"✅ Got diff ({len(diff)} chars)")

            if not diff.strip():
                print("⚠️ Empty diff, skipping review")
                return {"status": "skipped"}

            # Step 3: Send to Claude for review
            print(f"🤖 Sending diff to Claude...")
            comments = await review_diff(diff)
            print(f"✅ Claude returned {len(comments)} comments")

            # Step 4: Post comments back to PR
            if comments:
                await post_review(
                    repo_full_name=repo,
                    pr_number=pr_number,
                    commit_sha=details["commit_sha"],
                    comments=comments,
                    token=token
                )
                print(f"✅ Posted review to PR")
            else:
                print("ℹ️ No comments to post")

            # Step 5: Save to Cosmos DB
            await save_review(
                repo=repo,
                pr_number=pr_number,
                author=details["author"],
                title=details["title"],
                comments=comments
            )
            print(f"✅ Saved to Cosmos DB")

        except Exception as e:
            print(f"❌ Error during review: {e}")
            raise

    return {"status": "ok"}

@app.get("/reviews")
async def list_reviews():
    """Dashboard API — returns recent reviews"""
    reviews = await get_recent_reviews()
    return {"reviews": reviews}

@app.get("/health")
async def health():
    return {"status": "healthy"}