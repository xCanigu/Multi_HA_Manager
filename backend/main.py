from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

instances = {}  # {"instance_id": {"status": "...", "version": "..."}}
clients = {}    # {"instance_id": WebSocket}

class Heartbeat(BaseModel):
    instance_id: str
    status: str
    version: str

class Command(BaseModel):
    instance_id: str
    command: str

@app.post("/heartbeat")
async def heartbeat(data: Heartbeat):
    instances[data.instance_id] = {
        "status": data.status,
        "version": data.version
    }
    return {"message": "Heartbeat received"}

@app.get("/instances")
async def get_instances():
    return instances

@app.post("/commands")
async def send_command(command: Command):
    instance_id = command.instance_id
    cmd = command.command
    ws = clients.get(instance_id)
    if ws:
        await ws.send_text(cmd)
        return {"message": f"Command sent to {instance_id}"}
    else:
        return {"error": f"{instance_id} not connected"}

@app.websocket("/ws/{instance_id}")
async def websocket_endpoint(websocket: WebSocket, instance_id: str):
    await websocket.accept()
    clients[instance_id] = websocket
    try:
        while True:
            await websocket.receive_text()  # keep alive
    except WebSocketDisconnect:
        clients.pop(instance_id, None)
