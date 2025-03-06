# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlalchemy.future import select

# from db import get_db
# from models import User
# from .schemas import UserLogin, Token
# from .utils.hash import verify_password
# from .utils.auth import create_access_token


# router = APIRouter()

# @router.post("/login", response_model=Token)
# async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
#     result = await db.execute(select(User).where(User.email == user_data.email))
#     user = result.scalar()
    
#     if not user or not verify_password(user_data.password, user.password):
#         raise HTTPException(status_code=400, detail="Invalid credentials")
#     access_token = create_access_token({"sub": str(user.id)})
    
#     return {"access_token": access_token, "token_type": "bearer"}


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from models import User
from authentication import create_access_token, hash_password, verify_password
from .schemas import UserCreate
from datetime import timedelta
from sqlalchemy.future import select

router = APIRouter()

@router.post("/signup/")
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == user.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = await hash_password(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password, name=user.name)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return {"message": "User created successfully"}

@router.post("/login/")
async def login(email: str, password: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalar_one_or_none()
    
    if not user or not await verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = await create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
