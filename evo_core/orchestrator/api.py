from fastapi import FastAPI
from .orchestrator import Orchestrator
import threading

app = FastAPI()
orch = Orchestrator()
threading.Thread(target=orch.start, daemon=True).start()

@app.get("/health")
async def health():
    return {"status": "ok"}
