from app.redis_pubsub import RedisPubSub
from app.database import SessionLocal
from app.models import Message

class ChatManager:
    def __init__(self):
        self.connections = {}   #stores active WebSocket connections for each room
        self.redis = RedisPubSub()  #to use Redis pub/sub for broadcasting

    async def connect(self, websocket, room):
        await websocket.accept()
        self.connections.setdefault(room, []).append(websocket)
        await self.redis.subscribe(room, lambda msg: self.broadcast(room, msg))

    async def handle_message(self, room, message):
        await self.redis.publish(room, message) #publishes msg on redis so all receivers can recieve it
        db = SessionLocal()
        db.add(Message(room=room, content=message))
        db.commit()                             #saves msg to db
        db.close()

    async def broadcast(self, room, message):       #sends msg to all websocket clients in that room
        for ws in self.connections.get(room, []):
            await ws.send_text(message)

    async def disconnect(self, websocket, room):    #removes that websocket(user) from room
        self.connections[room].remove(websocket)
