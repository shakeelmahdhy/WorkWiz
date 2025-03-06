# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from models import User

from ..schemas import UserCreate

async def get_live_user(db: AsyncSession, user_id: int):
    query = select(User).filter(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Function to update the user's profile
async def update_user(db: AsyncSession, user_id: int, user_data: UserCreate):
    user = await get_current_user(db, user_id)
    user.email = user_data.email
    user.name = user_data.name
    if user_data.password:
        user.hashed_password = await hash_password(user_data.password)
    await db.commit()
    await db.refresh(user)
    return user