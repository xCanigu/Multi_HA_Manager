import asyncio
import websockets

INSTANCE_ID = "robot_1"
# SERVER_URL = f"ws://localhost:8000/ws/{INSTANCE_ID}"
SERVER_URL = "ws://localhost:8000/ws/robot_1"

async def listen_to_commands():
    async with websockets.connect(SERVER_URL) as websocket:
        print(f"[{INSTANCE_ID}] Connected to WebSocket server")
        try:
            while True:
                command = await websocket.recv()
                print(f"[{INSTANCE_ID}] Received command: {command}")
                # TODO: Execute command here
        except websockets.exceptions.ConnectionClosed:
            print(f"[{INSTANCE_ID}] WebSocket connection closed.")

if __name__ == "__main__":
    asyncio.run(listen_to_commands())
