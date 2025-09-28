# src/backend/app.py
"""
Configuración principal de la aplicación FastAPI.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from src.backend.config import settings
from src.backend.api.v1.router import api_router # Importamos el router principal
from src.backend.monitoring.health import health_router # Importamos router de health checks
from src.backend.monitoring.metrics import metrics_router # Importamos router de métricas

# lifespan se puede pasar directamente a FastAPI si se define aquí o importa
# Por simplicidad, lo dejamos en main.py y lo pasamos como parámetro
def create_app(lifespan=None):
    """Crea y configura la instancia de FastAPI."""

    app = FastAPI(
        title="AVTech Platform API",
        description="API para la gestión de contenido y pantallas digitales.",
        version="1.0.0",
        lifespan=lifespan,
        # Opcional: Documentación personalizada
        openapi_url="/api/v1/openapi.json",
        docs_url="/api/v1/docs", # URL para Swagger UI
        redoc_url="/api/v1/redoc", # URL para ReDoc
    )

    # --- Middlewares ---
    # CORS Middleware (ajusta los orígenes según tu frontend)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # TODO: Cambiar a dominios específicos en producción
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Trusted Host Middleware (ajusta los hosts según tu despliegue)
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"], # TODO: Cambiar a hosts específicos en producción
    )

    # --- Routers ---
    app.include_router(api_router, prefix="/api/v1") # Rutas principales de la API
    app.include_router(health_router, prefix="/api/v1") # Rutas de health check
    app.include_router(metrics_router, prefix="/api/v1") # Rutas de métricas (si aplica aquí)

    # Endpoint raíz simple
    @app.get("/")
    def read_root():
        return {"message": "Bienvenido a la API de AVTech Platform"}

    return app