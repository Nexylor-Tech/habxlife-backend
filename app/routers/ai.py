from fastapi import APIRouter, Depends
from ..services import ai_service
from ..schemas import HabitGenRequest
from ..deps import verify_access
from ..db import supabase

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/generate-habits")
def generate_habits(req: HabitGenRequest):
    return ai_service.generate_habits(req.goal)

@router.post("/summary")
def generate_summary(user = Depends(verify_access)):
    tasks = supabase.table('tasks').select('*').eq('user_id', user.id).execute().data
    return ai_service.generate_summary_from_tasks(tasks)