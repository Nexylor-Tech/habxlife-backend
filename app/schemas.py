from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

#Auth schemas
class UserCredentials(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr

class UserProfileUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    old_password: Optional[str] = None

#Task schemas
class TaskCreate(BaseModel):
    title: str
    deadline: datetime
    is_recurring: bool = Field(default=False)

class Task(TaskCreate):
    id: str
    created_at: datetime
    completed: bool
    user_id: str
    is_recurring: bool

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    deadline: Optional[datetime] = None
    completed: Optional[bool] = None
    is_recurring: Optional[bool] = None