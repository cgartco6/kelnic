# evo_core/orchestrator/orchestrator.py
from typing import Dict, Any, Optional
import structlog
from evo_core.memory.state_manager import StateManager
from evo_core.orchestrator.message_bus import MessageBus
from evo_core.agents.meta_agent import MetaAgent

logger = structlog.get_logger()

class KelnicOrchestrator:
    def __init__(self):
        self.state_manager = StateManager()
        self.message_bus = MessageBus()
        self.meta_agent = MetaAgent(self)
        self.agents = {}
        self.logger = logger.bind(component="KelnicOrchestrator")

    def register_agent(self, name: str, agent_instance):
        self.agents[name] = agent_instance
        self.logger.info(f"Agent registered: {name}")

    async def process_task(self, task: str, session_id: str, context: Dict[str, Any], priority: int = 5):
        self.logger.info("Processing task", task=task, session_id=session_id)

        # Save incoming context
        await self.state_manager.set_state(session_id, "current_task", task)

        # Let Meta Agent decide which specialized agent(s) to use
        plan = await self.meta_agent.route_task(task, context)

        self.logger.info("Meta agent routing plan", plan=plan)

        results = []

        for step in plan.get("steps", []):
            agent_name = step.get("agent")
            agent_task = step.get("task")

            if agent_name in self.agents:
                agent = self.agents[agent_name]
                try:
                    result = await agent.execute(agent_task, context)
                    results.append({"agent": agent_name, "result": result})
                    
                    # Publish event
                    await self.message_bus.publish(f"{agent_name}.completed", {
                        "session_id": session_id,
                        "task": agent_task,
                        "result": result
                    })
                except Exception as e:
                    self.logger.error(f"Agent {agent_name} failed", error=str(e))
                    results.append({"agent": agent_name, "error": str(e)})
            else:
                self.logger.warning(f"Agent not found: {agent_name}")

        # Save final result
        await self.state_manager.set_state(session_id, "last_result", results)

        return {
            "session_id": session_id,
            "task": task,
            "plan": plan,
            "results": results
        }
