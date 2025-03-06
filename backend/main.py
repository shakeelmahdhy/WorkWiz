from fastapi import FastAPI
from routes import auth, projects, tasks, users
import models
from db import async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

app = FastAPI(
    title = "task-manager",
    version = "0.0.1",
    contact = {
        "name": "Shakeel"
    }
)


app.include_router(auth.router, tags=["Auth"])
app.include_router(projects.router, tags=["Projects"])
app.include_router(tasks.router, tags=["Tasks"])
app.include_router(users.router, tags=["Users"])

@app.on_event("startup")
async def on_startup():
    await init_db()