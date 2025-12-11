from ..db import supabase
from ..schemas import TaskCreate, TaskUpdate, Task
from fastapi import HTTPException
from datetime import datetime, timedelta
from typing import List, Dict, Any


def create_task_for_user(task: TaskCreate, user_id: str) -> Dict[str, Any]:
    data = {
        'title': task.title,
        'deadline': task.deadline.isoformat() if isinstance(task.deadline, datetime) else task.deadline,
        'completed': False,
        'user_id': user_id,
        'is_recurring': task.is_recurring
    }
    res = supabase.table('tasks').insert(data).execute()
    if not res.data:
        raise HTTPException(status_code=400, detail="Failed to create task")
    return res.data[0]

def get_tasks_for_user(user_id: str) -> List[Dict[str, Any]]:
    res = supabase.table('tasks').select('*').eq('user_id', user_id).order('deadline').execute()
    return res.data or []


def update_task_for_user(task_id: str, task: TaskUpdate, user_id: str) -> Dict[str, Any]:
    current_task_res = supabase.table('tasks').select('*').eq('id', task_id).eq('user_id', user_id).execute()
    if not current_task_res.data:
        raise HTTPException(status_code=404, detail="Task not found")
    current_task = current_task_res.data[0]

    data = {k: v for k, v in task.dict().items() if v is not None}
    res = supabase.table('tasks').update(data).eq('id', task_id).eq('user_id', user_id).execute()
    updated_task = res.data[0]

    if (task.completed is True and not current_task['completed'] and updated_task['is_recurring']):
        old_deadline = datetime.fromisoformat(current_task['deadline'])
        new_deadline = old_deadline + timedelta(days=1)
        new_task_data = {
            'title': current_task['title'],
            'deadline': new_deadline.isoformat(),
            'completed': False,
            'user_id': user_id,
            'is_recurring': True
        }
        supabase.table('tasks').insert(new_task_data).execute()
    return updated_task



def delete_task_for_user(task_id: str, user_id: str) -> dict:
    res = supabase.table('tasks').delete().eq('id', task_id).eq('user_id', user_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Task not found")
    return {'msg': 'Task is successfully deleted'}
