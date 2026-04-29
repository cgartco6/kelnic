# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager
import structlog

from evo_core.orchestrator.orchestrator import KelnicOrchestrator
from evo_core.agents.agent_registry import register_all_agents
from evo_core.memory.state_manager import StateManager

# Import routes
from backend.routes import (
    marketing, finance, invoices, payments, payouts,
    metrics, qa, social, templates, webhooks, books, resources
)

logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info("🚀 Starting Kelnic AI Business OS...")

    # Initialize core systems
    app.state.orchestrator = KelnicOrchestrator()
    app.state.state_manager = StateManager()

    # Register all agents
    register_all_agents(app.state.orchestrator)

    logger.info("✅ Kelnic System Ready with Multi-Agent Orchestration")
    yield

    logger.info("🛑 Shutting down Kelnic...")

app = FastAPI(
    title="Kelnic",
    description="AI-Powered All-in-One Business Evolution Platform",
    version="0.2.0",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routes
app.include_router(marketing.router, prefix="/api/marketing", tags=["marketing"])
app.include_router(finance.router, prefix="/api/finance", tags=["finance"])
app.include_router(invoices.router, prefix="/api/invoices", tags=["invoices"])
app.include_router(payments.router, prefix="/api/payments", tags=["payments"])
app.include_router(payouts.router, prefix="/api/payouts", tags=["payouts"])
app.include_router(metrics.router, prefix="/api/metrics", tags=["metrics"])
app.include_router(qa.router, prefix="/api/qa", tags=["quality-assurance"])
app.include_router(social.router, prefix="/api/social", tags=["social"])
app.include_router(templates.router, prefix="/api/templates", tags=["templates"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["webhooks"])
app.include_router(books.router, prefix="/api/books", tags=["books"])
app.include_router(resources.router, prefix="/api/resources", tags=["resources"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Kelnic AI Business OS",
        "status": "running",
        "version": "0.2.0",
        "agents_registered": len(app.state.orchestrator.agents) if hasattr(app.state, "orchestrator") else 0
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "system": "Kelnic"}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
