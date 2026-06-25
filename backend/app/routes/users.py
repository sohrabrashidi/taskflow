from fastapi import APIRouter, HTTPException
from app.models import UserRegister, UserLogin, TokenResponse
from app.database import get_db
from app.auth import hash_password, verify_password, create_token
from datetime import datetime

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(user: UserRegister):
    db = get_db()
    if await db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=409, detail="Email already registered")
    doc = {"email": user.email, "name": user.name, "password": hash_password(user.password), "created_at": datetime.utcnow()}
    result = await db.users.insert_one(doc)
    return TokenResponse(access_token=create_token(str(result.inserted_id)))


@router.post("/login", response_model=TokenResponse)
async def login(creds: UserLogin):
    db = get_db()
    user = await db.users.find_one({"email": creds.email})
    if not user or not verify_password(creds.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenResponse(access_token=create_token(str(user["_id"])))
