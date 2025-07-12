from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.chat_manager import ChatManager
from app.models import Base
from app.database import engine

app = FastAPI()
chat = ChatManager()

@app.on_event("startup")        #runs when app starts
def startup():
    Base.metadata.create_all(bind=engine)   #creates messages table

@app.websocket("/ws/{room}")
async def chat_ws(websocket: WebSocket, room: str):
    await chat.connect(websocket, room)
    try:
        while True:
            msg = await websocket.receive_text()
            await chat.handle_message(room, msg)
    except WebSocketDisconnect:
        await chat.disconnect(websocket, room)

@app.get("/health")
def health():
    return {"status": "up"}
