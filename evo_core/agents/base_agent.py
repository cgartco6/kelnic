# evo_core/agents/base_agent.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import structlog
from datetime import datetime

logger = structlog.get_logger()

class BaseAgent(ABC):
    def __init__(self, name: str, description: str, orchestrator=None):
        self.name = name
        self.description = description
        self.orchestrator = orchestrator
        self.logger = logger.bind(agent=name)
        self.last_execution = None

    @abstractmethod
    async def execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Main execution method for the agent"""
        pass

    async def log_execution(self, task: str, status: str, result: Optional[Dict] = None):
        self.last_execution = {
            "timestamp": datetime.utcnow().isoformat(),
            "task": task,
            "status": status,
            "result_summary": str(result)[:200] if result else None
        }
        self.logger.info(f"Execution {status}", task=task)

    def get_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "last_execution": self.last_execution,
            "status": "active"
        }
