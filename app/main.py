from fastapi import FastAPI
from app.controllers.events import events_router


def create_app():
    app = FastAPI()
    app.include_router(events_router)
    return app


ems = create_app()