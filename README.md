# 🤖 AI Code Reviewer

> An AI-powered GitHub bot that automatically reviews pull requests using Claude AI, posts inline code comments with severity classification, and tracks review analytics on a dashboard — built with FastAPI, Azure Cosmos DB, and the Anthropic API.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green?logo=fastapi)
![Claude](https://img.shields.io/badge/Claude-Sonnet_4.5-purple?logo=anthropic)
![Azure](https://img.shields.io/badge/Azure-Cosmos_DB-0078D4?logo=microsoftazure)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

- **Automatic PR Reviews** — Triggers on every pull request opened or updated via GitHub webhooks
- **AI-Powered Analysis** — Sends PR diffs to Claude AI which detects bugs, security vulnerabilities, performance issues, and style suggestions
- **Inline Comments** — Posts review comments directly on the relevant lines of code in the PR
- **Severity Classification** — Each comment is tagged as 🔴 Error, 🟡 Warning, or 🔵 Suggestion
- **Review Summary** — Posts a structured summary table at the top of every review
- **Analytics Storage** — Persists every review to Azure Cosmos DB for dashboard reporting
- **Large PR Support** — Automatically chunks large diffs to handle PRs of any size

---

## 🏗️ Architecture

```
GitHub PR Opened / Updated
          │
          ▼
  GitHub Webhook (HTTPS)
          │
          ▼
  FastAPI Server (/webhook)
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
GitHub API   Anthropic
(fetch diff) (Claude AI)
    │           │
    │     Review Comments
    │           │
    └─────┬─────┘
          │
          ▼
  Post Inline PR Comments
  (GitHub Reviews API)
          │
          ▼
  Save Analytics
  (Azure Cosmos DB)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.11, FastAPI, Uvicorn |
| **AI** | Anthropic Claude Sonnet (claude-sonnet-4-5) |
| **GitHub Integration** | GitHub Apps, Webhooks, PyGithub |
| **Database** | Azure Cosmos DB (NoSQL, Serverless) |
| **Auth** | JWT (RS256), GitHub Installation Tokens |
| **HTTP Client** | httpx (async) |
| **Deployment** | Azure Functions *(coming soon)* |
| **CI/CD** | GitHub Actions *(coming soon)* |

---

## 📁 Project Structure

```
ai-code-reviewer/
├── backend/
│   ├── __init__.py
│   ├── main.py           # FastAPI app + webhook handler
│   ├── config.py         # Environment config
│   ├── models.py         # Pydantic schemas
│   ├── github_client.py  # GitHub API wrapper (auth, diff fetch, post review)
│   ├── llm_reviewer.py   # Claude AI integration + diff chunking
│   └── db.py             # Cosmos DB client + queries
├── frontend/             # Next.js dashboard (in progress)
├── infrastructure/       # Azure Bicep IaC (in progress)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- A GitHub account
- An [Anthropic API key](https://console.anthropic.com)
- An Azure account with a Cosmos DB instance
- Node.js (for smee.io webhook tunnel during local dev)

---

### 1. Clone the Repository

```bash
git clone https://github.com/sahilrox/ai-code-reviewer.git
cd ai-code-reviewer
```

### 2. Set Up Python Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Create a GitHub App

1. Go to **GitHub → Settings → Developer Settings → GitHub Apps → New GitHub App**
2. Set the following:
   - **Webhook URL:** Use [smee.io](https://smee.io/new) for local dev
   - **Permissions:** Pull requests (Read & Write), Contents (Read)
   - **Events:** Subscribe to `Pull request`
3. Generate and download a **private key** (.pem file)
4. Note your **App ID**
5. Install the app on your target repository

### 4. Set Up Azure Cosmos DB

1. Create a Cosmos DB account (Serverless mode recommended)
2. Create a database named `codereview`
3. Add a container named `reviews` with partition key `/repo`
4. Copy the **URI** and **Primary Key** from the Keys section

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# GitHub App
GITHUB_APP_ID=your_app_id
GITHUB_PRIVATE_KEY_PATH=./your-private-key.pem
GITHUB_WEBHOOK_SECRET=your_webhook_secret

# Anthropic
ANTHROPIC_API_KEY=your_anthropic_api_key

# Azure Cosmos DB
COSMOS_URL=https://your-account.documents.azure.com:443/
COSMOS_KEY=your_cosmos_primary_key

# App
PORT=8000
ENVIRONMENT=development
```

> ⚠️ Never commit your `.env` file or `.pem` file to version control.

### 6. Run the Server

```bash
uvicorn backend.main:app --reload --port 8000
```

### 7. Start the Webhook Tunnel

In a second terminal:

```bash
npm install -g smee-client
smee --url https://smee.io/your-channel --target http://localhost:8000/webhook
```

### 8. Test It

Open a pull request on your installed repository — the bot will automatically review it and post inline comments within seconds.

---

## 💬 Example Review Output

When a PR is opened, the bot posts a summary and inline comments like:

**Review Summary:**
| 🔴 Errors | 🟡 Warnings | 🔵 Suggestions |
|-----------|-------------|----------------|
| 4 | 1 | 1 |

**Inline comment examples:**

> 🔴 **ERROR**
> Division by zero is not handled. This will raise a `ZeroDivisionError` when `b=0`. Add a guard: `if b == 0: raise ValueError('Cannot divide by zero')`

> 🔴 **ERROR**
> SQL injection vulnerability. Never concatenate user input into queries. Use parameterized queries with proper parameter binding.

> 🟡 **WARNING**
> Potential information leak. Logging database connection strings can expose sensitive credentials. Log only sanitized connection info.

> 🔵 **SUGGESTION**
> Inefficient iteration pattern. Prefer a list comprehension: `return [item * 2 for item in items]`

---

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/webhook` | Receives GitHub webhook events |
| `GET` | `/reviews` | Returns recent review analytics |
| `GET` | `/health` | Health check |

---

## 🗺️ Roadmap

- [x] GitHub App webhook integration
- [x] Claude AI diff review with severity classification
- [x] Inline PR comment posting
- [x] Azure Cosmos DB analytics storage
- [ ] Next.js analytics dashboard
- [ ] Deploy to Azure Functions
- [ ] GitHub Actions CI/CD pipeline
- [ ] Support for multiple programming languages with language-specific prompts
- [ ] Per-repo configuration via `.ai-reviewer.yml`
- [ ] Slack/Teams notification integration

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

[MIT](LICENSE)

---

## 👤 Author

**Sahil** — [@sahilrox](https://github.com/sahilrox)

*Built as a portfolio project demonstrating full-stack development, cloud architecture, and AI integration.*
