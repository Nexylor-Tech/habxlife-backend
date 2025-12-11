from fastapi import APIRouter
from ..schemas import UserCredentials, UserResponse, UserProfileUpdate
from ..services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserResponse)
def signup(creds: UserCredentials):
    return auth_service.signup(creds)

@router.post("/login", response_model=UserResponse)
def login(creds: UserCredentials):
    return auth_service.login(creds)


@router.put("/profile/{user_id}")
def update_profile(user_id: str, update: UserProfileUpdate):
    return auth_service.update_profile(user_id, update)