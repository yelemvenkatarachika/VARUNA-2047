"""
VARUNA 2047 - Backend Application Entry Point
FastAPI application with OpenAPI docs, CORS, and endpoint mounting.
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.app.core.config import settings
from backend.app.api.router import router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Viksit Bharat Agricultural Resilience Using National Earth Observation - Backend API",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount satellite assets directory for static access if present
if os.path.exists(settings.SATELLITE_DIR):
    app.mount("/static/satellite", StaticFiles(directory=settings.SATELLITE_DIR), name="satellite")

# Mount API router
app.include_router(router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "project": settings.PROJECT_NAME,
        "tagline": settings.PROJECT_TAGLINE,
        "version": settings.VERSION,
        "documentation": "/docs",
        "api_endpoints": f"{settings.API_V1_STR}/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
