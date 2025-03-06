from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase

#synchronous
# DATABASE_URL = "postgresql+psycopg2://postgres:2005@localhost:2005/task-manager"

#async
DATABASE_URL = "postgresql+asyncpg://postgres:2005@localhost:2005/task-manager"

#synchronous
# engine = create_engine(
#     DATABASE_URL, connect_args={}, future=True
#     )

async_engine = create_async_engine(DATABASE_URL)

#synchronous
# SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)

SessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass

#db dependency

# def get_db():

#     db = SessionLocal()

#     try:
#         yield db
#     finally:
#         db.close()


# preferred code to avoid blocking of loop
async def get_db():
    async with SessionLocal() as session:
        yield session
        await session.commit()
