import threading
import asyncio

from fastapi import FastAPI

from .project.settings import settings
from .ws import router as ws_router
from .project.rabbit import events_rabbit


app = FastAPI(
    redoc_url='/api/v1/events/redoc' if settings.run_mode == 'dev' else None,
    docs_url='/api/v1/events/docs' if settings.run_mode == 'dev' else None,
)

app.include_router(ws_router, prefix='/api/v1/events/ws')


def events_target(loop: asyncio.AbstractEventLoop):
    asyncio.ensure_future(events_rabbit.listen(), loop=loop)


@app.on_event("startup")
async def on_startup():
    await events_rabbit.connect()
    loop = asyncio.get_running_loop()
    thread = threading.Thread(target=events_target, args=(loop,))
    thread.start()
