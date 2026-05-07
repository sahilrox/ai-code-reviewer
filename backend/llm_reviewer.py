import json
import asyncio
from anthropic import Anthropic
from backend.config import ANTHROPIC_API_KEY

client = Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """You are a senior software engineer performing a thorough code review.

Analyze the git diff and return a JSON array of review comments.
Each comment must have exactly these fields:
- "path": the file path being commented on (string)
- "line": the line number in the NEW file where the issue is (integer)
- "body": clear, actionable explanation of the issue and how to fix it (string)
- "severity": one of exactly "error", "warning", or "suggestion" (string)

Rules:
- "error": bugs, security vulnerabilities, data loss risks, crashes
- "warning": performance issues, bad practices, missing error handling
- "suggestion": style improvements, better naming, refactoring ideas

Only comment on real issues. Be specific and helpful.
Return ONLY a valid JSON array. No markdown, no explanation, no backticks."""

def chunk_diff(diff: str, max_chars: int = 12000) -> list[str]:
    if len(diff) <= max_chars:
        return [diff]
    
    chunks = []
    lines = diff.split("\n")
    current_chunk = []
    current_len = 0

    for line in lines:
        if current_len + len(line) > max_chars and current_chunk:
            chunks.append("\n".join(current_chunk))
            current_chunk = [line]
            current_len = len(line)
        else:
            current_chunk.append(line)
            current_len += len(line)

    if current_chunk:
        chunks.append("\n".join(current_chunk))

    return chunks

async def review_diff(diff: str) -> list[dict]:
    if not diff.strip():
        return []

    all_comments = []
    chunks = chunk_diff(diff)

    for i, chunk in enumerate(chunks):
        try:
            # Run sync Claude client in thread pool so it doesn't block async
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: client.messages.create(
                    model="claude-sonnet-4-5",
                    max_tokens=2000,
                    system=SYSTEM_PROMPT,
                    messages=[{
                        "role": "user",
                        "content": f"Review this PR diff (part {i+1} of {len(chunks)}):\n\n{chunk}"
                    }]
                )
            )

            raw = response.content[0].text.strip()

            if raw.startswith("```"):
                raw = raw.split("\n", 1)[1]  # remove first line (```json)
                raw = raw.rsplit("```", 1)[0]  # remove trailing ```
                raw = raw.strip()
            print(f"🤖 Claude raw response preview: {raw[:200]}")

            comments = json.loads(raw)

            for c in comments:
                if all(k in c for k in ["path", "line", "body", "severity"]):
                    all_comments.append(c)

        except json.JSONDecodeError as e:
            print(f"❌ JSON parse error on chunk {i+1}: {e}")
            print(f"Raw response was: {raw}")
            continue
        except Exception as e:
            print(f"❌ LLM error on chunk {i+1}: {e}")
            continue

    return all_comments