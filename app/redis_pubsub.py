import redis.asyncio as redis   #assume redis to be netflix to understand better
import asyncio      #asynchronous I/O

class RedisPubSub:
    def __init__(self):
        self.redis = redis.Redis(host="redis", port=6379, decode_responses=True)    #connects to Redis container (host = redis from Docker)

    async def publish(self, room: str, message: str):       #publishes a msg to a redis channel(room)
        await self.redis.publish(room, message)

    async def subscribe(self, room: str, callback):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(room)

        async def reader():
            async for msg in pubsub.listen():
                if msg["type"] == "message":
                    await callback(msg["data"])

        asyncio.create_task(reader())
