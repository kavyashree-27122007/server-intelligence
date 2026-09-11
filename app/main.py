"""
Main FastAPI Application Entrypoint for Support Intelligence.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import logger
from app.api.routes import router
from app.services.orchestrator import pipeline


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model artifacts and retrieval indices on startup."""
    logger.info("Initializing Support Intelligence Pipeline artifacts...")
    try:
        pipeline.load_artifacts()
        logger.info(f"Support Intelligence Pipeline ready for brand: {settings.brand}")
    except Exception as e:
        logger.error(f"Failed to load pipeline artifacts: {e}")
    yield
    logger.info("Shutting down Support Intelligence Pipeline.")


app = FastAPI(
    title="Support Intelligence API",
    description="Evidence-Grounded Customer Support Decision Engine",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API endpoints
app.include_router(router)

# Mount Frontend SPA if built
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

DIST_DIR = settings.project_root / "frontend" / "dist"

if (DIST_DIR / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(DIST_DIR / "assets")), name="assets")

if DIST_DIR.exists():
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api/"):
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail=f"API route /{full_path} not found")
        target = DIST_DIR / full_path
        if target.is_file():
            return FileResponse(target)
        return FileResponse(DIST_DIR / "index.html")
else:
    @app.get("/")
    async def root():
        return {
            "service": "Support Intelligence API",
            "brand": settings.brand,
            "docs": "/docs",
            "health": "/api/health",
            "version": "1.0.0",
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api.host,
        port=settings.api.port,
        reload=settings.debug,
    )
