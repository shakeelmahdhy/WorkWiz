from typing import List

from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from .schemas import Task, TaskCreate
from .utils.projects import get_project
from .utils.tasks import get_task, get_tasks, create_task, delete_task
from dependencies import get_current_user

router = APIRouter()

@router.post("/tasks", response_model=Task)
async def create_new_task(
    task: TaskCreate, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    return await create_task(db, task, owner_id=current_user["id"])

@router.get("/tasks", response_model=List[Task])
async def get_all_tasks(
    skip: int = 0, 
    limit: int = 10, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    tasks = await get_tasks(db, skip, limit, owner_id=current_user["id"])
    return tasks

# Route to get a task by its ID
@router.get("/tasks/{task_id}", response_model=Task)
async def get_task_by_id(
    task_id: int, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    task = await get_task(db, task_id, owner_id=current_user["id"])
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Route to update a task
@router.put("/tasks/{task_id}", response_model=Task)
async def update_task_details(
    task_id: int, 
    task_data: TaskCreate, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    return await update_task(db, task_id, task_data, current_user["id"])

# Route to delete a task
@router.delete("/tasks/{task_id}")
async def delete_task_endpoint(
    task_id: int, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    return await delete_task(db, task_id, current_user["id"])