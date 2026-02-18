from fastapi import HTTPException
from .database import get_user, add_user
from .utils import generate_token

tokens = {}  # {token: username}

def register_user(username: str, password: str):
    existing = get_user(username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists.")
    add_user(username, password)
    return {"message": "User registered successfully"}

def login_user(username: str, password: str):
    user = get_user(username)
    if not user or user[2] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = generate_token()
    tokens[token] = username
    return {"token": token}

def authenticate_token(token: str):
    if token not in tokens:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return tokens[token]
