from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency pentru a folosi DB în endpointuri
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
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
async def heartbeat(data: Heartbeat, db: Session = Depends(get_db)):
    instance = db.query(models.Instance).filter(models.Instance.instance_id == data.instance_id).first()

    if instance:
        instance.status = data.status
        instance.version = data.version
        instance.last_heartbeat = datetime.utcnow()
    else:
        instance = models.Instance(
            instance_id=data.instance_id,
            status=data.status,
            version=data.version,
            last_heartbeat=datetime.utcnow()
        )
        db.add(instance)

    db.commit()
    instances[data.instance_id] = {
        "status": data.status,
        "version": data.version
    }
    return {"message": "Heartbeat saved to DB"}


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

@app.get("/instances_db")
def get_instances_db(db: Session = Depends(get_db)):
    db_instances = db.query(models.Instance).all()
    return [
        {
            "instance_id": inst.instance_id,
            "status": inst.status,
            "version": inst.version,
            "last_heartbeat": inst.last_heartbeat.isoformat()
        }
        for inst in db_instances
    ]
