from azure.cosmos import CosmosClient, exceptions
from backend.config import COSMOS_URL, COSMOS_KEY
from datetime import datetime, timezone

client = CosmosClient(COSMOS_URL, COSMOS_KEY)
db = client.get_database_client("codereview")
reviews_container = db.get_container_client("reviews")

async def save_review(
    repo: str,
    pr_number: int,
    author: str,
    title: str,
    comments: list[dict]
):
    errors = sum(1 for c in comments if c["severity"] == "error")
    warnings = sum(1 for c in comments if c["severity"] == "warning")
    suggestions = sum(1 for c in comments if c["severity"] == "suggestion")

    item = {
        "id": f"{repo.replace('/', '-')}-pr-{pr_number}",
        "repo": repo,
        "pr_number": pr_number,
        "author": author,
        "title": title,
        "comment_count": len(comments),
        "error_count": errors,
        "warning_count": warnings,
        "suggestion_count": suggestions,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    reviews_container.upsert_item(item)
    print(f"Saved review for {repo} PR#{pr_number} to Cosmos DB")
    return item

async def get_recent_reviews(limit: int = 20) -> list[dict]:
    query = f"SELECT TOP {limit} * FROM c ORDER BY c.timestamp DESC"
    items = list(reviews_container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    return items