from fastapi import APIRouter, Depends, HTTPException
from ..schemas import TaskCreate, TaskUpdate, Task
from ..services import task_service
from ..deps import get_current_user_id
from typing import List

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("", response_model=Task)
def create_task(task: TaskCreate, user_id: str = Depends(get_current_user_id)):
    return task_service.create_task_for_user(task, user_id)

@router.get("", response_model=List[Task])
def get_tasks(user_id: str = Depends(get_current_user_id)):
    return task_service.get_tasks_for_user(user_id)

@router.put("/{task_id}", response_model=Task)
def update_task(task_id: str, task: TaskUpdate, user_id: str = Depends(get_current_user_id)):
    return task_service.update_task_for_user(task_id, task, user_id)

@router.delete("/{task_id}")
def delete_task(task_id: str, user_id: str = Depends(get_current_user_id)):
    return task_service.delete_task_for_user(task_id, user_id)