from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict
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
    theme: Optional[str] = None
    timezone: Optional[str] = None

#Refresh Login
class RefreshTokenRequest(BaseModel):
    refresh_token: str

#Onboarding Update
class OnboardingUpdate(BaseModel):
    goal: Optional[str] = None
    generated_habits: Optional[List[Dict[str, str]]] = None
    selected_habits: Optional[List[str]] = None
    current_step: Optional[str] = None

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
    is_recurring: bool = False
    completed_at: Optional[datetime] = None

class TaskUpdate(BaseModel):
    completed: Optional[bool] = None


#AI Schemas
class HabitGenRequest(BaseModel):
    goal: str

#Payment Schemas
class CheckoutRequest(BaseModel):
    habits: List[str]
    duration_months: int

class PaymentRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    duration_months: int
