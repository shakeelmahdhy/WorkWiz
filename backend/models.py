from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy_utils import EmailType
from db import Base
from mixins import TimeStamp


class User(TimeStamp, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(EmailType, unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(String(100), index=True, nullable=True)
    is_active = Column(Boolean, default=True)
    projects = relationship("Project", back_populates="owner")
    tasks = relationship("Task", back_populates="owner")

class Project(TimeStamp, Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable = True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")


class Task(TimeStamp, Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default="to-do")
    due_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project = relationship("Project", back_populates="tasks")
    owner = relationship("User", back_populates="tasks")