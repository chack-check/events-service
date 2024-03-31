import asyncio
import logging
import threading

import sentry_sdk
from fastapi import FastAPI

from app.gql.router import router as gql_router
from app.project.settings import settings

from .project.rabbit import events_rabbit

logger = logging.getLogger("uvicorn.error")

logger.debug(f"Initializing sentry with dsn: {settings.sentry_dsn}")
if settings.sentry_dsn:
    sentry_sdk.init(settings.sentry_dsn)

app = FastAPI(redoc_url=None, docs_url=None, openapi_url=None)

app.include_router(gql_router, prefix="/api/v1/events")


def events_target(loop: asyncio.AbstractEventLoop):
    asyncio.ensure_future(events_rabbit.listen(), loop=loop)


@app.on_event("startup")
async def on_startup():
    await events_rabbit.connect()
    loop = asyncio.get_running_loop()
    thread = threading.Thread(target=events_target, args=(loop,))
    thread.start()
