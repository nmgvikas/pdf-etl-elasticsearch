# auth_controller.py
from fastapi import APIRouter, Depends
from datetime import timedelta
from auth import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(username: str, password: str):
    # Dummy check: replace with real user validation
    if username == "admin" and password == "admin":
        access_token = create_access_token({"sub": username}, timedelta(minutes=60))
        return {"access_token": access_token, "token_type": "bearer"}
    return {"error": "Invalid credentials"}
