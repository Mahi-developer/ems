from sqlalchemy import ScalarResult, select, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, DeclarativeMeta
from typing import Type, TypeVar, Optional, Any

from app.core.config import settings


engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)
Base = declarative_base()

# helpers
T = TypeVar("T", bound=DeclarativeMeta)

async def create(session: AsyncSession, model: Type[T], request_in) -> Optional[T]:
    obj = model(**request_in.model_dump())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

async def get_by_id(session: AsyncSession, model: Type[T], obj_id: int) -> Optional[T]:
    return await session.scalar(select(model).where(model.id == obj_id))

async def fetch_all_with_pagination(
    session: AsyncSession, model: Type[T], page: int = 0, limit: int = settings.PAGINATION_LIMIT
) -> ScalarResult[Any]:
    return await session.scalars(select(model).offset(page).limit(limit))

async def get_count(session: AsyncSession, model: Type[T]) -> Optional[T]:
    return await session.scalar(select(func.count()).select_from(model))
