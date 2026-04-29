# evo_core/memory/state_manager.py
import json
import redis.asyncio as redis
from typing import Dict, Any, Optional
from datetime import datetime
import structlog

logger = structlog.get_logger()

class StateManager:
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.redis = redis.from_url(redis_url, decode_responses=True)
        self.logger = logger.bind(component="StateManager")

    async def set_state(self, session_id: str, key: str, value: Any, ttl: int = 3600):
        """Save state with TTL (default 1 hour)"""
        try:
            data = {
                "value": value,
                "timestamp": datetime.utcnow().isoformat()
            }
            await self.redis.hset(f"session:{session_id}", key, json.dumps(data))
            await self.redis.expire(f"session:{session_id}", ttl)
            self.logger.info("State saved", session_id=session_id, key=key)
        except Exception as e:
            self.logger.error("Failed to save state", error=str(e))

    async def get_state(self, session_id: str, key: str) -> Optional[Any]:
        """Retrieve state"""
        try:
            data = await self.redis.hget(f"session:{session_id}", key)
            if data:
                return json.loads(data)["value"]
            return None
        except Exception as e:
            self.logger.error("Failed to get state", error=str(e))
            return None

    async def get_full_session(self, session_id: str) -> Dict[str, Any]:
        """Get entire session state"""
        try:
            data = await self.redis.hgetall(f"session:{session_id}")
            return {k: json.loads(v)["value"] for k, v in data.items()}
        except Exception:
            return {}

    async def clear_session(self, session_id: str):
        await self.redis.delete(f"session:{session_id}")
        self.logger.info("Session cleared", session_id=session_id)
