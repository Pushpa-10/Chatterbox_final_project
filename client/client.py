import asyncio
import websockets
import json
import requests

API_URL = "http://127.0.0.1:8000"

async def chat_client():
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Try login, else register
    res = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
    if res.status_code != 200:
        print("User not found, registering a new account...")
        requests.post(f"{API_URL}/register", json={"username": username, "password": password})
        res = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
    token = res.json()["token"]

    ws_url = f"ws://127.0.0.1:8000/ws/{token}"
    async with websockets.connect(ws_url) as websocket:
        print("✅ Connected to Chatterbox!")
        async def receive():
            while True:
                msg = await websocket.recv()
                print(msg)
        asyncio.create_task(receive())

        while True:
            message = input("> ")
            await websocket.send(message)

if __name__ == "__main__":
    asyncio.run(chat_client())
