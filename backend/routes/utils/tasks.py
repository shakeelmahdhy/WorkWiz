from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from datetime import datetime
from models import Task, Project
from ..schemas import TaskCreate


async def create_task(db: AsyncSession, task: TaskCreate, owner_id: int):
    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status or "to-do",
        due_date=task.due_date,
        project_id=task.project_id,
        owner_id=owner_id
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

async def get_task(db: AsyncSession, task_id: int, owner_id: int):
    query = select(Task).filter(Task.id == task_id, Task.owner_id == owner_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_tasks(db: AsyncSession, skip: int = 0, limit: int = 10, owner_id: int = None):
    query = select(Task).filter(Task.owner_id == owner_id).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def update_task(db: AsyncSession, task_id: int, task_data: TaskCreate, owner_id: int):
    task = await get_task(db, task_id, owner_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.title = task_data.title
    task.description = task_data.description
    task.status = task_data.status or task.status
    task.due_date = task_data.due_date
    task.project_id = task_data.project_id or task.project_id
    await db.commit()
    await db.refresh(task)
    return task

async def delete_task(db: AsyncSession, task_id: int, owner_id: int):
    task = await get_task(db, task_id, owner_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    await db.delete(task)
    await db.commit()
    return {"message": "Task deleted successfully"}