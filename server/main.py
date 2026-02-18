from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles # Optional: to serve HTML
from .database import init_db, get_recent_messages
from .auth import register_user, login_user, authenticate_token
from .models import UserRegister, UserLogin
from .websocket_manager import ConnectionManager

app = FastAPI(title="Chatterbox WebSocket Chat")
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"]
)

manager = ConnectionManager()

@app.post("/register")
async def register(user: UserRegister):
    # Pass attributes directly from the Pydantic model
    return register_user(user.username, user.password)

@app.post("/login")
async def login(user: UserLogin):
    # Pass attributes directly from the Pydantic model
    return login_user(user.username, user.password)

@app.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    username = authenticate_token(token)
    if not username:
        await websocket.close(code=1008) # Policy Violation
        return

    await manager.connect(websocket, username)
    
    # Send history to the new user
    recent = get_recent_messages()
    for u, msg, ts in reversed(recent):
        await websocket.send_text(f"[{ts}] {u}: {msg}")

    try:
        while True:
            msg = await websocket.receive_text()
            # Assuming handle_message handles both DB saving and broadcasting
            await manager.handle_message(username, msg)
    except WebSocketDisconnect:
        manager.disconnect(username)
        await manager.broadcast(f"⚠️ {username} left the chat.")

# To serve your index.html at the root URL:
# app.mount("/", StaticFiles(directory="static", html=True), name="static")
from fastapi.responses import FileResponse
import os

# Get the directory where main.py is located
current_dir = os.path.dirname(os.path.realpath(__file__))

@app.get("/")
async def get_index():
    return FileResponse(os.path.join(current_dir, "index.html"))