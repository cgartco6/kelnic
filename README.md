# Kelnic

**AI-Powered Business Evolution Platform**

An all-in-one intelligent system featuring 30+ specialized AI agents that automate marketing, finance, legal, design, sales, support, and business growth.

### Features
- Multi-Agent Orchestration System
- Self-healing & Self-improving architecture
- Meta Agent for intelligent task routing
- Full business automation (invoicing, payouts, marketing, content, etc.)
- Tiered product delivery system

### Tech Stack
- **Backend**: FastAPI + Python 3.11+
- **Agents**: LangGraph + LangChain
- **Frontend**: Next.js 15 (App Router)
- **Memory**: Redis + State Manager
- **Orchestration**: Custom Message Bus

### Quick Start

```bash
cp .env.example .env
# Edit .env with your keys

pip install -r requirements.txt
uvicorn backend.main:app --reload
