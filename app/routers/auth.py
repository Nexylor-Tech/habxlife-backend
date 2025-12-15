from fastapi import APIRouter, Depends, HTTPException
from ..schemas import UserCredentials, UserProfileUpdate, HabitGenRequest, OnboardingUpdate, RefreshTokenRequest
from ..services import auth_service
from ..deps import get_current_user_id
from ..db import supabase 

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup")
def signup(creds: UserCredentials):
    return auth_service.signup_with_password(creds)

@router.post("/login")
def login(creds: UserCredentials):
    return auth_service.login_with_password(creds)

@router.get("/me")
def me(user = Depends(get_current_user_id)):
    profile_res = supabase.table('profiles').select('*').eq('id', user.id).single().execute().data
    user_dict = {
        'id': user.id,
        'email': user.email,
        'profile': profile_res
    }
    return user_dict

@router.post("/refresh")
def refresh_token(req: RefreshTokenRequest):
    return auth_service.refresh_session(req)

@router.put("/profile/{user_id}")
def update_profile(user_id: str, update: UserProfileUpdate):
    return auth_service.update_profile(user_id, update)


@router.post("/onboarding/update")
def update_onboarding(update: OnboardingUpdate, user = Depends(get_current_user_id)):
    data = {}
    if update.goal is not None: data['goal'] = update.goal
    if update.generated_habits is not None: data['generated_habits'] = update.generated_habits
    if update.selected_habits is not None: data['selected_habits'] = update.selected_habits
    if update.current_step is not None: data['current_step'] = update.current_step

    if not data:
        return {'message': 'No changes'}
    try:
        supabase.table('profiles').update(data).eq('id', user.id).execute()
        return {'message': 'Progress saved'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save progress {str(e)}")