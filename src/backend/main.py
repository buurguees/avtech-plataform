"""
AVTech Platform - Backend Main Application
==========================================

FastAPI application for AVTech Platform backend services.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager

from src.backend.config import settings
from src.backend.database.connection import init_db
from src.backend.monitoring.logger import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    setup_logging()
    await init_db()
    yield
    # Shutdown
    pass


# Create FastAPI application
app = FastAPI(
    title="AVTech Platform API",
    description="Backend API for AVTech Platform - Digital Signage Management System",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AVTech Platform API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "avtech-backend"
    }


# Include API routes
# from src.backend.api.v1.router import api_router
# app.include_router(api_router, prefix="/api/v1")


def main():
    """Main entry point for the application."""
    uvicorn.run(
        "main:app",
        host=settings.server.host,
        port=settings.server.port,
        reload=settings.server.debug,
        log_level=settings.server.log_level.lower()
    )


if __name__ == "__main__":
    main()
