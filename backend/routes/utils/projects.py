

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import Project
from ..schemas import ProjectCreate



async def get_project(db: AsyncSession, name: str, owner_id: int):
    query = select(Project).where(Project.name==name, Project.owner_id==owner_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def create_project(db: AsyncSession, project: ProjectCreate, owner_id: int):
    new_project = Project(
        name=project.name, 
        description=project.description, 
        owner_id=owner_id
    )
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return new_project

async def get_projects(db: AsyncSession, skip: int = 0, limit: int = 10, owner_id: int = None):
    query = select(Project).filter(Project.owner_id == owner_id).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def update_project(db: AsyncSession, project_id: int, project_data: ProjectCreate, owner_id: int):
    project = await db.get(Project, project_id)
    if not project or project.owner_id != owner_id:
        raise HTTPException(status_code=403, detail="Unauthorized or project not found")
    
    project.name = project_data.name
    project.description = project_data.description
    await db.commit()
    await db.refresh(project)
    return project

async def delete_project(db: AsyncSession, project_id: int, owner_id: int):
    project = await db.get(Project, project_id)
    if not project or project.owner_id != owner_id:
        raise HTTPException(status_code=403, detail="Unauthorized or project not found")
    
    await db.delete(project)
    await db.commit()
    return {"message": "Project deleted successfully"}