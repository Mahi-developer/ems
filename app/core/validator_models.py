from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime, timezone


# noinspection PyNestedDecorators
class EventCreate(BaseModel):
    """
    Table model to store and retrieve event related data.
    """
    name: str = Field(max_length=255)
    location: str = Field(max_length=100)
    start_time: datetime
    end_time: datetime
    max_capacity: int

    class Config:
        from_attributes = True

    @field_validator('start_time')
    @classmethod
    def validate_start_time(cls, v):
        if v < datetime.now(tz=timezone.utc):
            raise ValueError('start_time must be in the future')
        return v

    @field_validator('end_time')
    @classmethod
    def validate_end_time(cls, v, info):
        start = info.data.get('start_time')
        if start and v <= start:
            raise ValueError('end_time must be after start_time')
        return v


class PaginatedEventResponse(BaseModel):
    data: list[EventCreate]
    count: int
    page: int


class UserBase(BaseModel):
    name: str = Field(max_length=255)
    email: EmailStr = Field(max_length=255)

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    event_id: int | None = None


class UsersPublic(BaseModel):
    data: list[UserBase]
    count: int
    page: int