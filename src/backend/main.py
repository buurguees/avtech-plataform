# src/backend/main.py
"""
Punto de entrada principal para la aplicación FastAPI del backend.
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.backend.config import settings
from src.backend.app import create_app
from src.backend.database.connection import init_db

# Configurar logging básico
logging.basicConfig(level=settings.server.log_level.upper())

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Contexto de vida útil de la aplicación FastAPI.
    Se ejecuta al inicio y al apagado.
    """
    print("Iniciando aplicación AVTech Backend...")
    # Inicializar recursos al inicio
    await init_db() # Inicializar conexión a la base de datos
    print("Conexión a la base de datos inicializada.")
    yield # Aquí corre la aplicación
    print("Cerrando aplicación AVTech Backend...")
    # Cerrar recursos al apagado si es necesario
    # await close_db_resources()

def main():
    """Función principal para ejecutar la aplicación."""
    app = create_app(lifespan=lifespan)
    import uvicorn
    uvicorn.run(
        app,
        host=settings.server.host,
        port=settings.server.port,
        reload=settings.server.debug, # Recarga automática en modo debug
        log_level=settings.server.log_level.lower()
    )

if __name__ == "__main__":
    main()