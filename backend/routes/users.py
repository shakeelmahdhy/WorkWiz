
from typing import List

from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from .schemas import User, UserCreate
from .utils.users import get_live_user, update_user
from dependencies import get_current_user
router = APIRouter()


@router.get("/users/myprofile", response_model=User)
async def get_user_profile(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return await get_live_user(db, current_user["id"])

@router.put("/users/myprofile", response_model=User)
async def update_user_profile(
    user_data: UserCreate, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    return await update_user(db, current_user["id"], user_data)