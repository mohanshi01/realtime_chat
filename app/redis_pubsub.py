import redis.asyncio as redis   #assume redis to be netflix to understand better
import asyncio      #asynchronous I/O

class RedisPubSub:
    def __init__(self):
        self.redis = redis.Redis(host="redis", port=6379, decode_responses=True)    #connects to Redis container (host = redis from Docker)

    async def publish(self, room: str, message: str):       #publishes a msg to a redis channel(room)
        await self.redis.publish(room, message)

    async def subscribe(self, room: str, callback):
        pubsub = self.redis.pubsub()    #creates a pubsub listener which lets user listen to published msgs in redis channels(chat rooms)
        await pubsub.subscribe(room)  #not this coz it raises a runtimewarning if no callback(a func to be called back if something happens or this is completed) is supplied.

        async def reader():             #listens to new messages on pubsub connection
            async for msg in pubsub.listen():
                if msg["type"] == "message":
                    await callback(msg["data"])    #calls that dummy callback

        asyncio.create_task(reader())   #starts reader func in background(asynchronously)
