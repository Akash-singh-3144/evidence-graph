from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

from fastapi import Request
from fastapi.responses import JSONResponse
import traceback

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_msg = f"{type(exc).__name__}: {str(exc)}"
    tb = traceback.format_exc()
    logger.error(f"Global exception: {error_msg}\n{tb}")
    return JSONResponse(
        status_code=500,
        content={"detail": error_msg, "traceback": tb}
    )

@app.on_event("startup")
async def startup_event():
    from app.rag.vectorstore.collections import init_qdrant
    try:
        await init_qdrant()
        logger.info("Qdrant collection schema initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize Qdrant collections: {e}")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[url.strip() for url in settings.FRONTEND_URLS.split(",") if url.strip()],
    allow_origin_regex=r"https://.*\.vercel\.app",
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
