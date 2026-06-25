from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from bson import ObjectId


class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Literal["low", "medium", "high"] = "medium"
    status: Literal["todo", "in_progress", "done"] = "todo"
    due_date: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[Literal["low", "medium", "high"]] = None
    status: Optional[Literal["todo", "in_progress", "done"]] = None
    due_date: Optional[datetime] = None


class TaskOut(TaskCreate):
    id: str
    user_id: str
    created_at: datetime


class UserRegister(BaseModel):
    email: str
    password: str = Field(..., min_length=8)
    name: str


class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
