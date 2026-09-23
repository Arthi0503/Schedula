"""Main FastAPI Application Entrypoint for Schedula."""
import time
from typing import Dict, Any

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False
    class FastAPI:  # type: ignore
        def __init__(self, *args, **kwargs): pass
        def include_router(self, *args, **kwargs): pass
        def add_middleware(self, *args, **kwargs): pass
        def get(self, *args, **kwargs):
            def d(f): return f
            return d

from app.core.config import settings
from app.api.endpoints import router as timetable_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Production-grade timetable clash detection, scheduling optimization, and Excel processing engine.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

if HAS_FASTAPI:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(timetable_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["Health & Status"])
def health_check() -> Dict[str, Any]:
    """Health check endpoint to verify backend operational readiness."""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "timestamp": time.time(),
        "engine": "active"
    }

@app.get("/", tags=["Root"])
def root() -> Dict[str, Any]:
    """Root metadata and navigation endpoint."""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs",
        "api_v1": f"{settings.API_V1_STR}/timetable"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
