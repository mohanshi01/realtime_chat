import redis.asyncio as redis
import asyncio

class RedisPubSub:
    def __init__(self):
        self.redis = redis.Redis(host="redis", port=6379, decode_responses=True)

    async def publish(self, room: str, message: str):
        await self.redis.publish(room, message)

    async def subscribe(self, room: str, callback):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(room)

        async def reader():
            async for msg in pubsub.listen():
                if msg["type"] == "message":
                    await callback(msg["data"])

        asyncio.create_task(reader())
