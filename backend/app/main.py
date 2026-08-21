from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": settings.PROJECT_NAME}

from app.api.routes import investigations, sources

app.include_router(investigations.router, prefix="/api/investigations", tags=["investigations"])
app.include_router(sources.router, prefix="/api/sources", tags=["sources"])
