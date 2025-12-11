from fastapi import Header, HTTPException

async def get_current_user_id(x_user_id: str = Header(..., description="User ID from login")) -> str:
    if not x_user_id:
        raise HTTPException(status_code=401, detail="X-User-ID header missing")
    return x_user_id