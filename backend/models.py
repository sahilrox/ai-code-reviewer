from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReviewComment(BaseModel):
    path: str
    line: int
    body: str
    severity: str  # "error" | "warning" | "suggestion"

class PRReview(BaseModel):
    id: str
    repo: str
    pr_number: int
    author: str
    title: str
    comment_count: int
    error_count: int
    warning_count: int
    suggestion_count: int
    timestamp: str