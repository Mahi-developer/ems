from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select

# module imports
from app.deps import get_db_session, SessionDep
from app.models import Event, User
from app.core.db import create, get_count, fetch_all_with_pagination
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


@events_router.post(
    "/{event_id}/register",
    dependencies=[Depends(get_db_session)],
    response_model=UserCreate
)
async def register_attendee(event_id: int, user_in: UserCreate, session: SessionDep):
    event = await session.scalar(select(Event).where(Event.id == event_id))
    if not event:
        raise HTTPException(status_code=400, detail="Oops! No event found.")

    stmt = (
        select(
            func.count(User.id).label("registered_count"),
            func.bool_or(User.email == user_in.email).label("is_registered")
        ).where(User.event_id == event_id)
    )
    result = await session.execute(stmt)
    row = result.first()
    registered_count, is_registered = row.registered_count, row.is_registered

    if registered_count == event.max_capacity:
        raise HTTPException(status_code=400, detail="Oops! Houseful.")

    if is_registered:
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

    attendees = await session.scalars(select(User).where(User.event_id == event_id).offset(page * limit).limit(limit))
    return UsersPublic(data=attendees, count=count, page=page)
