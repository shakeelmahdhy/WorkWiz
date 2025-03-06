from typing import List

from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from .schemas import Project, ProjectCreate
from .utils.projects import get_project, get_projects, create_project, update_project, delete_project
from dependencies import get_current_user


router = APIRouter()


@router.get("/project", response_model=List[Project])
async def read_projects(
    skip: int = 0,
    limit: int = 10, 
    db: AsyncSession = Depends(get_db),
    currents_user: dict = Depends(get_current_user)
):
    projects = await get_projects(db=db, skip=skip, limit=limit, owner_id=current_user["id"])
    return projects

@router.post("/project")
async def create_new_proj(
    project: ProjectCreate, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    db_proj = await get_project(db=db, name=project.name, owner_id=current_user["id"])
    if db_proj:
        raise HTTPException(status_code=400, detail="Project with this name already exists")
    return await create_project(db=db, project=project, owner_id=current_user["id"])

@router.get("/project/{name}")
async def read_project(name: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_proj = await get_project(db=db, name=name, owner_id=current_user["id"])
    if not db_proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_proj

@router.put("/project/{project_id}", response_model=Project)
async def update_project_details(
    project_id: int, 
    project_data: ProjectCreate, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    return await update_project(db, project_id, project_data, current_user["id"])

@router.delete("/project/{project_id}")
async def delete_project_endpoint(
    project_id: int, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    return await delete_project(db, project_id, current_user["id"])