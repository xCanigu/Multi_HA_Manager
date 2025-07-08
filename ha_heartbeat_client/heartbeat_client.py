import sys
import requests
import time
import asyncio
import websockets
import subprocess

server_url = sys.argv[1]
token = sys.argv[2]

async def listen_for_commands():
    async with websockets.connect(f"{server_url.replace('http', 'ws')}/ws",
                                   extra_headers={"Authorization": f"Bearer {token}"}) as ws:
        while True:
            cmd = await ws.recv()
            # Exemplu: execută local comanda primită
            if cmd == "update_ha":
                subprocess.run(["ha", "core", "update"])
                await ws.send("Update started")
            elif cmd == "restart_ha":
                subprocess.run(["ha", "core", "restart"])
                await ws.send("Restart done")

def send_heartbeat():
    while True:
        payload = {"status": "online"}
        headers = {"Authorization": f"Bearer {token}"}
        try:
            requests.post(f"{server_url}/heartbeat", json=payload, headers=headers)
        except Exception as e:
            print(e)
        time.sleep(30)

# Run: heartbeat + WS listener
async def main():
    await asyncio.gather(
        asyncio.to_thread(send_heartbeat),
        listen_for_commands()
    )

asyncio.run(main())
