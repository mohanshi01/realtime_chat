from app.redis_pubsub import RedisPubSub
from app.database import SessionLocal
from app.models import Message

class ChatManager:
    def __init__(self):
        self.connections = {}
        self.redis = RedisPubSub()

    async def connect(self, websocket, room):
        await websocket.accept()
        self.connections.setdefault(room, []).append(websocket)
        await self.redis.subscribe(room, lambda msg: self.broadcast(room, msg))

    async def handle_message(self, room, message):
        await self.redis.publish(room, message)
        db = SessionLocal()
        db.add(Message(room=room, content=message))
        db.commit()
        db.close()

    async def broadcast(self, room, message):
        for ws in self.connections.get(room, []):
            await ws.send_text(message)

    async def disconnect(self, websocket, room):
        self.connections[room].remove(websocket)
