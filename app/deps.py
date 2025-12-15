from fastapi import Header, HTTPException, Depends
from typing import Any
from .db import  supabase
from datetime import datetime, timezone 
from supabase import create_client
from .config import settings

async def get_user_token(authorization: str = Header(...)) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Token Format")
    return authorization.split(" ", 1)[1]


async def get_current_user_id(token: str = Depends(get_user_token)) -> Any:
    try:
        res = supabase.auth.get_user(token)
        if not res.user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return res.user
    except Exception as e:
        raise HTTPException(status_code=402, detail="Access Expired, Payment Needed")
    
async def verify_access(user = Depends(get_current_user_id)):
    profile = supabase.table('profiles').select('subscription_expiry').eq('id', user.id).single().execute().data
    if profile and profile.get('subscription_expiry'):
        expiry = datetime.fromisoformat(profile.get('subscription_expiry'))
        if datetime.now(timezone.utc) < expiry:
            return user
    raise HTTPException(status_code=402, detail="Access Expired, Payment Needed")


def get_auth_client(token: str):
    client = create_client(str(settings.SUPABASE_URL), str(settings.SUPABASE_API_KEY.get_secret_value()))
    client.postgrest.auth(token)
    return client

