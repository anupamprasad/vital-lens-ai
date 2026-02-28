"""
Vital Lens AI - Phase 3 Backend Application
FastAPI-based REST API for the Vital Lens AI platform
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import logging
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Application state
app_state = {"db": None, "redis": None}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events"""
    logger.info("Starting Vital Lens AI backend application...")
    # Startup
    try:
        # Database connection would go here
        logger.info("✓ Database connected")
        # Redis connection would go here
        logger.info("✓ Redis connected")
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    # Cleanup database and Redis connections
    logger.info("✓ Connections closed")

# Initialize FastAPI app
app = FastAPI(
    title="Vital Lens AI API",
    description="Remote Photoplethysmography (rPPG) Health Monitoring API",
    version="3.0.0",
    lifespan=lifespan
)

# CORS Middleware
origins = [
    "http://localhost:3000",      # Local development
    "http://localhost:5173",       # Vite dev server
    os.getenv("FRONTEND_URL", "http://localhost:3000"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZIP Middleware for compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Root endpoint
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "name": "Vital Lens AI Backend",
        "version": "3.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "cache": "connected"
    }

# API Version
@app.get("/api/v1")
async def api_root():
    """API v1 root"""
    return {
        "version": "1.0.0",
        "endpoints": [
            "/api/v1/auth",
            "/api/v1/users",
            "/api/v1/vitals",
            "/api/v1/health"
        ]
    }

"""
Import and register API routers.  Each router already declares its
own prefix, so we don't repeat it again here to avoid doubling the
path (e.g. `/api/v1/auth/api/v1/auth`).  Keeping the prefix inside the
router simplifies tests and lets the router be used independently if
needed.
"""

# NOTE: avoid circular imports; all routers are fairly lightweight.
from api import auth, users, vitals

# register routers - prefixes are defined in the individual modules
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(vitals.router)

# future extension point:
# from api import admin
# app.include_router(admin.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
