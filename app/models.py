from datetime import datetime

from pydantic import EmailStr
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, func, TIMESTAMP, ForeignKey
from sqlalchemy.orm import declarative_mixin

from app.core.db import Base


@declarative_mixin
class BaseModelMixin:
    """
    Base Model class with necessary common fields used.
    """
    id = Column(Integer, primary_key=True, index=True)
    created_dtm = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified_dtm = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Event(Base, BaseModelMixin):
    """
    Table model to store and retrieve event related data.
    """
    __tablename__ = "events"

    name = Column(String(255), index=True, nullable=False)
    location = Column(String(150), index=True, nullable=False)
    start_time = Column(TIMESTAMP(timezone=True), nullable=False)
    end_time = Column(TIMESTAMP(timezone=True), nullable=False)
    max_capacity = Column(Integer, nullable=False)
    users = relationship("User", back_populates="events")


class User(Base, BaseModelMixin):
    __tablename__ = "users"
    name = Column(String(255), index=True, nullable=False)
    email: EmailStr = Column(String(255), index=True, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    events = relationship("Event", back_populates="users")
