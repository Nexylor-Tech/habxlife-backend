from ..db import supabase
from ..schemas import TaskCreate, TaskUpdate, Task
from ..deps import get_auth_client 
from fastapi import HTTPException
from datetime import datetime, timedelta
from typing import List, Dict, Any

def get_tasks_for_user(user: str, token: str) -> List[Dict[str, Any]]:
    client = get_auth_client(token)
    res = client.table('tasks').select('*').eq('user_id', user).order('deadline').execute()
    return res.data


def create_task_for_user(task, user: str, token: str) -> Dict[str, Any]:
    client = get_auth_client(token)
    data = {
        'title': task.title,
        'deadline': task.deadline.isoformat(),
        'completed': False,
        'user_id': user,
        'is_recurring': task.is_recurring
    }
    res = client.table('tasks').insert(data).execute()
    if not res.data:
        raise HTTPException(status_code=400, detail="Failed to create task")
    return res.data[0]



def update_task_for_user(task_id: str, task: TaskUpdate, user: str, token: str) -> Dict[str, Any]:
    client = get_auth_client(token)


    res = client.table('tasks').select('*').eq('id', task_id).eq('user_id', user).single().execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Task not found")

    current_task = res.data
    if current_task['completed'] and not task.completed:
        raise HTTPException(status_code=400, detail="Task is already completed")

    data = {'completed': task.completed}
    if task.completed:
        data['completed_at'] = datetime.now().isoformat()
    
    updated = client.table('tasks').update(data).eq('id', task_id).execute().data[0]
    if task.completed and updated['is_recurring']:
        new_deadline = datetime.fromisoformat(current_task['deadline']) + timedelta(days=1)
        client.table('tasks').insert({
            'title': current_task['title'],
            'deadline': new_deadline.isoformat(),
            'completed': False,
            'user_id': user,
            'is_recurring': True
        }).execute()
    return updated



def delete_task_for_user(task_id: str, user_id: str, token: str) -> dict:
    client = get_auth_client(token)
    res = client.table('tasks').delete().eq('id', task_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Task not found")
    return {'msg': 'Task is successfully deleted'}
