from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.backend.config import settings
import logging

logger = logging.getLogger(__name__)

# Crear el motor de base de datos async
engine = create_async_engine(
    settings.database.url,
    echo=settings.database.echo, # Log de SQL si está habilitado
    pool_pre_ping=True, # Verifica la conexión antes de usarla
)

# Crear la clase de sesión asincrónica
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db_session() -> AsyncSession:
    """
    Generator para obtener una sesión de base de datos.
    Se usa como dependencia en FastAPI.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Opcional: Función para inicializar la base de datos (crear tablas si es necesario)
async def init_db():
    # Importar modelos para que SQLAlchemy los registre
    from src.backend.database import models # Asegura que los modelos estén cargados
    from sqlalchemy.ext.asyncio import AsyncEngine
    from sqlalchemy import event
    from sqlalchemy.dialects.postgresql import dialect

    async with engine.begin() as conn:
        # Opción 1: Usar Alembic para migraciones (recomendado para producción)
        # await conn.run_sync(Base.metadata.create_all) # No usar directamente con Alembic
        # Opción 2: Crear tablas directamente (solo para desarrollo o pruebas simples)
        # from src.backend.database.models import Base # Asegura que Base esté importado
        # await conn.run_sync(Base.metadata.create_all)

        # Para integración con Alembic, normalmente se usa el comando `alembic upgrade head`
        # o se corre un script de migración separado.
        logger.info("Conexión a la base de datos inicializada.")