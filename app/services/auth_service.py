from ..db import supabase, supabase_admin
from fastapi import HTTPException
from ..schemas import UserCredentials, UserProfileUpdate 

def signup(creds: UserCredentials):
    try:
        res = supabase.auth.sign_up({"email": creds.email, "password": creds.password})
        print(res)
        if not res.user:
            raise HTTPException(status_code=400, detail="Signup failed")
        return {"id": res.user.id, "email": res.user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def login(creds: UserCredentials):
    try:
        res = supabase.auth.sign_in_with_password({"email": creds.email, "password": creds.password})
        print(res)
        if res.user is None:
            raise HTTPException(status_code=400, detail="Invalid credentials")
        return {"id": res.user.id, "email": res.user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
def update_profile(user_id: str, update: UserProfileUpdate):
    if not supabase_admin:
        raise HTTPException(status_code=500, detail="Admin client not initialized")
    
    if update.email:
        try:
            supabase_admin.auth.admin.update_user_by_id(user_id, {'email': update.email})
            return {"message": "Email updated successfully"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed {str(e)}")
    

    if update.password:
        if not update.old_password:
            raise HTTPException(status_code=400, detail="Old password required to update")
        try:
            user_data = supabase_admin.auth.admin.get_user_by_id(user_id)
            supabase.auth.sign_in_with_password({"email": user_data.user.email, "password": update.old_password})
        except Exception as e:
            raise HTTPException(status_code=403, detail="Old password is incorrect")


        try:
            supabase_admin.auth.admin.update_user_by_id(user_id, {'password': update.password})
            return {"message": "Password updated successfully"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))