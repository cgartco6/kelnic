---

### 5. `backend/main.py` (Full Code)

```python
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager

from evo_core.orchestrator.orchestrator import KelnicOrchestrator
from evo_core.memory.state_manager import StateManager
from backend.routes import books, finance, invoices, marketing, metrics, payments, payouts, qa, resources, social, templates, webhooks

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting Kelnic AI Business OS...")
    app.state.orchestrator = KelnicOrchestrator()
    app.state.state_manager = StateManager()
    yield
    # Shutdown
    print("🛑 Shutting down Kelnic...")

app = FastAPI(
    title="Kelnic",
    description="AI Multi-Agent Business Evolution Platform",
    version="0.1.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routes
app.include_router(books.router, prefix="/api/books", tags=["books"])
app.include_router(finance.router, prefix="/api/finance", tags=["finance"])
app.include_router(invoices.router, prefix="/api/invoices", tags=["invoices"])
app.include_router(marketing.router, prefix="/api/marketing", tags=["marketing"])
app.include_router(metrics.router, prefix="/api/metrics", tags=["metrics"])
app.include_router(payments.router, prefix="/api/payments", tags=["payments"])
app.include_router(payouts.router, prefix="/api/payouts", tags=["payouts"])
app.include_router(qa.router, prefix="/api/qa", tags=["quality-assurance"])
app.include_router(resources.router, prefix="/api/resources", tags=["resources"])
app.include_router(social.router, prefix="/api/social", tags=["social"])
app.include_router(templates.router, prefix="/api/templates", tags=["templates"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["webhooks"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Kelnic AI",
        "status": "running",
        "version": "0.1.0",
        "agents": "30+ specialized AI agents ready"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
