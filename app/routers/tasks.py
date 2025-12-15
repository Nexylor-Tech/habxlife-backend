from fastapi import APIRouter, Depends, HTTPException
from ..schemas import TaskCreate, TaskUpdate, Task
from ..services import task_service
from ..deps import get_current_user_id, verify_access, get_user_token, get_user_token
from typing import List

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("", response_model=Task)
def create_task(task: TaskCreate, user = Depends(verify_access), token: str = Depends(get_user_token)):
    return task_service.create_task_for_user(task, user.id, token)

@router.get("", response_model=List[Task])
def get_tasks(user = Depends(verify_access), token: str = Depends(get_user_token)):
    return task_service.get_tasks_for_user(user.id, token)

@router.put("/{task_id}", response_model=Task)
def update_task(task_id: str, task: TaskUpdate, user = Depends(verify_access), token: str = Depends(get_user_token)):
    return task_service.update_task_for_user(task_id, task, user.id, token)

@router.delete("/{task_id}")
def delete_task(task_id: str, user = Depends(verify_access), token: str = Depends(
    get_user_token)):
    return task_service.delete_task_for_user(task_id, user.id, token)