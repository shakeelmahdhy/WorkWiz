from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


#-----------------------------------

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    ...

class Project(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


#----------------------------------

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "to-do"
    due_date: datetime
    project_id: Optional[int] = None

class TaskCreate(TaskBase):
    ...

class Task(TaskBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


#----------------------------------


class UserBase(BaseModel):
    email: str
    name: str
    password: str
    role: Optional[str] = "user"

class UserCreate(UserBase):
    ...

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        exclude = {"password", "hashed_password"}

