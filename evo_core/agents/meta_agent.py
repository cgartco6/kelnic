# evo_core/agents/meta_agent.py
from typing import Dict, Any, List
from evo_core.agents.base_agent import BaseAgent

class MetaAgent(BaseAgent):
    def __init__(self, orchestrator):
        super().__init__(
            name="MetaAgent",
            description="Intelligent router and planner for all Kelnic agents",
            orchestrator=orchestrator
        )
        self.available_agents = {}

    def register_agent(self, name: str, description: str):
        self.available_agents[name] = description

    async def route_task(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Decide which agent(s) should handle the task"""
        
        # Simple but effective routing logic (you can later replace with LLM call)
        task_lower = task.lower()

        plan = {"steps": []}

        if any(word in task_lower for word in ["market", "campaign", "advertise", "promote", "social"]):
            plan["steps"].append({
                "agent": "MarketingEngineAgent",
                "task": task
            })

        if any(word in task_lower for word in ["finance", "budget", "expense", "revenue", "profit"]):
            plan["steps"].append({
                "agent": "FinancialAgent",
                "task": task
            })

        if any(word in task_lower for word in ["invoice", "billing", "payment request"]):
            plan["steps"].append({
                "agent": "InvoicingAgent",
                "task": task
            })

        if any(word in task_lower for word in ["pay", "payout", "transfer", "withdraw"]):
            plan["steps"].append({
                "agent": "PayoutAgent",
                "task": task
            })

        if any(word in task_lower for word in ["content", "write", "script", "blog", "email"]):
            plan["steps"].append({
                "agent": "ContentCreatorAgent",
                "task": task
            })

        # Default fallback
        if not plan["steps"]:
            plan["steps"].append({
                "agent": "SupportAgent",
                "task": f"General assistance for: {task}"
            })

        plan["reasoning"] = f"Routed based on keyword analysis for task: {task}"
        plan["priority"] = 5

        return plan
