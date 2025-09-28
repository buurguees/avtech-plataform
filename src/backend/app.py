"""
AVTech Platform - Backend Application Factory
============================================

Application factory for creating FastAPI instances.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from src.backend.config import settings


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    
    app = FastAPI(
        title="AVTech Platform API",
        description="Backend API for AVTech Platform - Digital Signage Management System",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc"
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

    return app


# Create application instance
app = create_app()
