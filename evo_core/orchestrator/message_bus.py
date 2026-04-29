# evo_core/orchestrator/message_bus.py
from typing import Dict, Any, Callable, Awaitable
import asyncio
import structlog
from datetime import datetime

logger = structlog.get_logger()

class MessageBus:
    def __init__(self):
        self.subscribers: Dict[str, list[Callable[[Dict[str, Any]], Awaitable[None]]]] = {}
        self.logger = logger.bind(component="MessageBus")

    def subscribe(self, event_type: str, handler: Callable[[Dict[str, Any]], Awaitable[None]]):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)
        self.logger.info(f"Handler subscribed to {event_type}")

    async def publish(self, event_type: str, payload: Dict[str, Any]):
        payload["timestamp"] = datetime.utcnow().isoformat()
        payload["event_type"] = event_type

        self.logger.info(f"Event published: {event_type}", payload=payload)

        if event_type in self.subscribers:
            for handler in self.subscribers[event_type]:
                try:
                    await handler(payload)
                except Exception as e:
                    self.logger.error(f"Handler failed for {event_type}", error=str(e))
