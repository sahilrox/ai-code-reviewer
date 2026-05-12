# 🤖 AI Code Reviewer

> An AI-powered GitHub bot that automatically reviews pull requests using Claude AI, posts inline code comments with severity classification, and tracks review analytics on a live dashboard — built with FastAPI, Azure Container Apps, and the Anthropic API.

[![Deploy Backend](https://github.com/sahilrox/ai-code-reviewer/actions/workflows/deploy-backend.yml/badge.svg)](https://github.com/sahilrox/ai-code-reviewer/actions/workflows/deploy-backend.yml)
[![Deploy Frontend](https://github.com/sahilrox/ai-code-reviewer/actions/workflows/deploy-frontend.yml/badge.svg)](https://github.com/sahilrox/ai-code-reviewer/actions/workflows/deploy-frontend.yml)
[![PR Checks](https://github.com/sahilrox/ai-code-reviewer/actions/workflows/pr-checks.yml/badge.svg)](https://github.com/sahilrox/ai-code-reviewer/actions/workflows/pr-checks.yml)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green?logo=fastapi)
![Claude](https://img.shields.io/badge/Claude-Sonnet_4.5-purple)
![Azure](https://img.shields.io/badge/Azure-Container_Apps-0078D4?logo=microsoftazure)
![Next.js](https://img.shields.io/badge/Next.js-15-black?logo=nextdotjs)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🌐 Live Demo

| Service | URL |
|---------|-----|
| **Dashboard** | [ai-code-reviewer-swart-gamma.vercel.app](https://ai-code-reviewer-swart-gamma.vercel.app) |
| **API Health** | [/health](https://ai-code-reviewer-api.delightfulcoast-1c596bb9.centralindia.azurecontainerapps.io/health) |
| **API Reviews** | [/reviews](https://ai-code-reviewer-api.delightfulcoast-1c596bb9.centralindia.azurecontainerapps.io/reviews) |

---

## 📸 Dashboard Preview

![AI Code Reviewer Dashboard](./docs/dashboard.png)

---

## ✨ Features

- **Automatic PR Reviews** — Triggers on every pull request opened or updated via GitHub webhooks
- **AI-Powered Analysis** — Sends PR diffs to Claude AI which detects bugs, security vulnerabilities, performance issues, and style suggestions
- **Inline Comments** — Posts review comments directly on the relevant lines of code in the PR
- **Severity Classification** — Each comment tagged as 🔴 Error, 🟡 Warning, or 🔵 Suggestion
- **Review Summary** — Posts a structured summary table at the top of every review
- **Analytics Dashboard** — Live Next.js dashboard with charts showing review trends, severity breakdown, and author stats
- **Analytics Storage** — Persists every review to Azure Cosmos DB (serverless)
- **Large PR Support** — Automatically chunks large diffs to handle PRs of any size
- **CI/CD Pipeline** — GitHub Actions auto-deploys backend to Azure and verifies frontend on every push to main

---

## 🏗️ Architecture

```
GitHub PR Opened / Updated
          │
          ▼
  GitHub Webhook (HTTPS)
          │
          ▼
  FastAPI Server
  (Azure Container Apps)
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
          │
          ▼
  Next.js Dashboard
  (Vercel)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.11, FastAPI, Uvicorn |
| **AI** | Anthropic Claude Sonnet 4.5 |
| **GitHub Integration** | GitHub Apps, Webhooks, REST API |
| **Database** | Azure Cosmos DB (NoSQL, Serverless) |
| **Frontend** | Next.js 15, TypeScript, Tailwind CSS, Recharts |
| **Auth** | JWT (RS256), GitHub Installation Tokens |
| **Deployment** | Azure Container Apps, Vercel |
| **Registry** | Azure Container Registry |
| **CI/CD** | GitHub Actions |

---

## 📁 Project Structure

```
ai-code-reviewer/
├── .github/
│   └── workflows/
│       ├── deploy-backend.yml   # Auto-deploy backend to Azure on push
│       ├── deploy-frontend.yml  # Verify frontend build on push
│       └── pr-checks.yml        # Syntax + type checks on every PR
├── backend/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app + webhook handler
│   ├── config.py                # Environment config
│   ├── models.py                # Pydantic schemas
│   ├── github_client.py         # GitHub API wrapper
│   ├── llm_reviewer.py          # Claude AI integration + diff chunking
│   ├── rate_limiter.py          # Request rate limiting
│   └── db.py                    # Cosmos DB client
├── frontend/
│   ├── app/
│   │   ├── page.tsx             # Main dashboard page
│   │   └── globals.css          # Global styles + animations
│   ├── components/
│   │   ├── StatsBar.tsx         # Stats cards (8 metrics)
│   │   ├── Charts.tsx           # Recharts visualizations
│   │   └── ReviewsTable.tsx     # Recent reviews table
│   └── lib/
│       └── api.ts               # API client
├── docs/
│   └── dashboard.png            # Dashboard screenshot
├── Dockerfile
├── .dockerignore
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- A GitHub account
- An [Anthropic API key](https://console.anthropic.com)
- An Azure account with Cosmos DB

### 1. Clone the Repository

```bash
git clone https://github.com/sahilrox/ai-code-reviewer.git
cd ai-code-reviewer
```

### 2. Set Up Python Environment

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

### 3. Create a GitHub App

1. Go to **GitHub → Settings → Developer Settings → GitHub Apps → New GitHub App**
2. Set permissions: Pull requests (Read & Write), Contents (Read)
3. Subscribe to `Pull request` events
4. Generate and download a private key (.pem)
5. Install the app on your target repository

### 4. Set Up Azure Cosmos DB

1. Create a Cosmos DB account (Serverless mode)
2. Create database `codereview` with container `reviews` (partition key `/repo`)
3. Copy the URI and Primary Key

### 5. Configure Environment Variables

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

### 6. Run Locally

```bash
# Terminal 1 — Backend
uvicorn backend.main:app --reload --port 8000

# Terminal 2 — Webhook tunnel
smee --url https://smee.io/your-channel --target http://localhost:8000/webhook

# Terminal 3 — Frontend
cd frontend && npm run dev
```

Open [http://localhost:3000](http://localhost:3000) for the dashboard.

---

## 🚢 Deployment

### Backend — Azure Container Apps

```bash
# Build and push image
az acr build --registry aicodereviewer --image ai-code-reviewer:latest .

# Deploy
az containerapp update \
  --name ai-code-reviewer-api \
  --resource-group ai-code-reviewer-rg \
  --image aicodereviewer.azurecr.io/ai-code-reviewer:latest
```

### Frontend — Vercel

Connect your GitHub repo to Vercel, set root directory to `frontend`, and add `NEXT_PUBLIC_API_URL` environment variable pointing to your Azure Container App URL.

### CI/CD

Every push to `main` automatically:
1. Runs syntax and type checks
2. Builds Docker image tagged with commit SHA
3. Pushes to Azure Container Registry
4. Deploys new revision to Azure Container Apps
5. Vercel auto-deploys frontend changes

---

## 💬 Example Review Output

When a PR is opened the bot posts a summary and inline comments:

**Review Summary:**
| 🔴 Errors | 🟡 Warnings | 🔵 Suggestions |
|-----------|-------------|----------------|
| 4 | 1 | 1 |

**Inline comments:**

> 🔴 **ERROR** — Division by zero not handled. Add: `if b == 0: raise ValueError('Cannot divide by zero')`

> 🔴 **ERROR** — SQL injection vulnerability. Use parameterized queries instead of string concatenation.

> 🟡 **WARNING** — Logging database connection strings can expose sensitive credentials in logs.

> 🔵 **SUGGESTION** — Use a list comprehension: `return [item * 2 for item in items]`

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
- [x] Next.js analytics dashboard with live charts
- [x] Deploy backend to Azure Container Apps
- [x] Deploy frontend to Vercel
- [x] GitHub Actions CI/CD pipeline
- [x] Rate limiting utility
- [ ] Per-repo configuration via `.ai-reviewer.yml`
- [ ] Language-specific review prompts
- [ ] Slack/Teams notification integration
- [ ] Weekly digest email reports

---

## 🤝 Contributing

Pull requests are welcome. The PR Checks workflow will automatically run syntax and type checks on your contribution.

---

## 📄 License

[MIT](LICENSE)

---

## 👤 Author

**Sahil** — [@sahilrox](https://github.com/sahilrox)

*Built as a portfolio project demonstrating full-stack development, cloud architecture, AI integration, and DevOps practices.*
