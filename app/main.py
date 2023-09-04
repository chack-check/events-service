from fastapi import FastAPI

from .project.settings import settings
from .ws import router as ws_router


app = FastAPI(
    redoc_url = '/api/v1/events/redoc' if settings.run_mode == 'dev' else None,
    docs_url = '/api/v1/events/docs' if settings.run_mode == 'dev' else None,
)

app.include_router(ws_router, prefix='/api/v1/events/ws')
