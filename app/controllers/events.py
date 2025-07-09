from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select

# module imports
from app.deps import get_db_session, SessionDep
from app.models import Event, User
from app.core.db import create, get_count, get_by_id, fetch_all_with_pagination
from app.core.validator_models import EventCreate, PaginatedEventResponse, UserCreate, UsersPublic
from app.core.config import settings

events_router = APIRouter(prefix="/events", tags=["events"],)


# async define events related routes
@events_router.get("/ping")
def ping():
    """
    Ping Check
    :return str: pong
    :return:
    """
    return "pong"


# noinspection PyArgumentList
@events_router.post(
    "/",
    dependencies=[Depends(get_db_session)],
    response_model=EventCreate
)
async def create_event(event_in: EventCreate, session: SessionDep):
    """
    Creates new event with the request
    :return json: success / validation response
    """
    event = await create(session, model=Event, request_in=event_in)
    return event


@events_router.get(
    "/",
    dependencies=[Depends(get_db_session)],
    response_model=PaginatedEventResponse
)
async def fetch_events(session: SessionDep, page: int = 0, limit: int = settings.PAGINATION_LIMIT):
    count = await get_count(session, model=Event)
    events = await fetch_all_with_pagination(session, model=Event, page=page, limit=limit)
    return PaginatedEventResponse(data=events, count=count, page=page)


@events_router.get(
    "/{event_id}/register",
    dependencies=[Depends(get_db_session)],
    response_model=UserCreate
)
async def register_attendee(event_id: int, user_in: UserCreate, session: SessionDep):
    event = await get_by_id(session, model=Event, obj_id=event_id)
    if not event:
        raise HTTPException(status_code=400, detail="Oops! No event found.")

    if len(event.users) == event.max_capacity:
        raise HTTPException(status_code=400, detail="Oops! Houseful.")

    user = await session.scalar(select(User).where(User.event_id == event_id, User.email == user_in.email))
    if not user:
        raise HTTPException(status_code=400, detail="Oops! User already registered")

    user_in.event_id = event_id
    return await create(session, model=User, request_in=user_in)


@events_router.get(
    "/{event_id}/attendees",
    dependencies=[Depends(get_db_session)],
    response_model=UsersPublic
)
async def fetch_events(event_id: int, session: SessionDep, page: int = 0, limit: int = settings.PAGINATION_LIMIT):
    count = await session.scalar(
        select(func.count()).select_from(User).where(User.event_id == event_id)
    )

    attendees = await session.scalars(select(User).where(User.event_id == event_id).offset(page).limit(limit))
    return UsersPublic(data=attendees, count=count, page=page)
