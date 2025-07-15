import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "up"}

def test_websocket_echo():
    with client.websocket_connect("/ws/testroom") as ws:
        ws.send_text("Hello world")
        msg = ws.receive_text()
        assert msg == "Hello world"
