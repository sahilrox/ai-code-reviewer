import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_APP_ID = os.getenv("GITHUB_APP_ID")
GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
COSMOS_URL = os.getenv("COSMOS_URL", "")
COSMOS_KEY = os.getenv("COSMOS_KEY", "")

# Support both file path and direct key content
GITHUB_PRIVATE_KEY_PATH = os.getenv("GITHUB_PRIVATE_KEY_PATH", "")
GITHUB_PRIVATE_KEY_CONTENT = os.getenv("GITHUB_PRIVATE_KEY_CONTENT", "")

if GITHUB_PRIVATE_KEY_CONTENT:
    # Used in production — key passed directly as env var
    GITHUB_PRIVATE_KEY = GITHUB_PRIVATE_KEY_CONTENT.replace("\\n", "\n")
elif GITHUB_PRIVATE_KEY_PATH:
    # Used in local dev — key loaded from .pem file
    with open(GITHUB_PRIVATE_KEY_PATH, "r") as f:
        GITHUB_PRIVATE_KEY = f.read()
else:
    raise ValueError("Either GITHUB_PRIVATE_KEY_PATH or GITHUB_PRIVATE_KEY_CONTENT must be set")