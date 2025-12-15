from ..db import supabase, supabase_admin
from fastapi import HTTPException
from ..schemas import UserCredentials, UserProfileUpdate 
from typing import Dict, Any 

def signup_with_password(creds: UserCredentials) -> Dict[str, Any]:
    try:
        res = supabase.auth.sign_up({
            'email': creds.email,
            'password': creds.password,
        })
        if not res.user:
            raise HTTPException(status_code=400, detail='User not found')
        try:
            supabase.table('profiles').insert({
                'id': res.user.id,
                'email': res.user.email,
                'onboarding_completed': False,
                'current_step': 'goal',
                'theme': 'light',
            }).execute()
        except Exception as e:
            print('Account creation failed')
            raise HTTPException(status_code=400, detail={e})
        
        if res.session:
            return res.session

        try:
            login_res = supabase.auth.sign_in_with_password({
                'email': creds.email,
                'password': creds.password
            })
            if login_res.session:
                return login_res.session
        except:
            pass
        
        return {'message': 'User created successfully Please sign in'}

    except Exception as e:
        raise HTTPException(status_code=400, detail={e})


def login_with_password(creds: UserCredentials) -> Dict[str, Any]:
    try:
        res = supabase.auth.sign_in_with_password({
            'email': creds.email,
            'password': creds.password,
        })
        if not res.session:
            raise HTTPException(status_code=400, detail={'Invalid Credential'})
        return res.session
    except Exception as e:
        raise HTTPException(status_code=400, detail={'Login Failed. Invalid credentials'})

#validate token between session 
def refresh_session(req):
    try:
        res = supabase.auth.refresh_session(req)
        if not res.session:
            raise HTTPException(status_code=400, detail={'Invalid Credential'})
        return res.session
    except Exception as e:
        raise HTTPException(status_code=400, detail={'Refresh Failed. Invalid credentials'})


def update_profile(user: str, update: UserProfileUpdate):
    if not supabase_admin:
        raise HTTPException(status_code=500, detail="Admin client not initialized")
    
    updates: Dict[str, Any] = {}

    if update.theme:
        supabase.table('profiles').update({
            'theme': update.theme
        }).eq('id', user).execute()
    return {'message': 'Updated'}

    if update.email:
        try:
            supabase_admin.auth.admin.update_user_by_id(user, {'email': update.email})
            updates['email'] = update.email
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed {str(e)}")

    if update.password:
        if not update.old_password:
            raise HTTPException(status_code=400, detail="Old password required to update")
        try:
            user_data = supabase_admin.auth.admin.get_user_by_id(user)
            supabase.auth.sign_in_with_password({"email": user_data.user.email, "password": update.old_password})
        except Exception as e:
            raise HTTPException(status_code=403, detail="Old password is incorrect")


        try:
            supabase_admin.auth.admin.update_user_by_id(user, {'password': update.password})
            updates['password'] = "updated"
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    return updates  