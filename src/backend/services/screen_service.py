# src/backend/services/screen_service.py
"""
Servicio de negocio para la gestión de pantallas.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.database.models import ScreenCreate, ScreenResponse, ScreenUpdate, ScreenStatus
from src.backend.database.repository import ScreenRepository # Asumimos que se creará
from src.backend.exceptions.sync_exceptions import ScreenProvisioningException # Asumimos que se creará
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ScreenService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.screen_repo = ScreenRepository(db_session)

    async def create_screen(self, screen_data: ScreenCreate) -> ScreenResponse:
        """Crea una nueva pantalla."""
        logger.info(f"Creando pantalla: {screen_data.name}")
        # Aquí se podría validar el provisioning_token si se usa para aprovisionamiento
        # y marcar la pantalla como 'provisioning' temporalmente.
        # Tambien se asume que created_at, updated_at se manejan en la DB o aquí.
        db_screen = {
            "name": screen_data.name,
            "location": screen_data.location,
            "client_id": screen_data.client_id,
            "status": screen_data.status,
            "last_heartbeat": screen_data.last_heartbeat,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        try:
            created_screen_db = await self.screen_repo.create(db_screen)
        except Exception as e:
            logger.error(f"Error al crear pantalla {screen_data.name}: {e}")
            raise ScreenProvisioningException(f"Error al registrar la pantalla: {str(e)}")

        response_screen = ScreenResponse(
            screen_id=created_screen_db.id,
            name=created_screen_db.name,
            location=created_screen_db.location,
            client_id=created_screen_db.client_id,
            status=created_screen_db.status,
            last_heartbeat=created_screen_db.last_heartbeat,
            created_at=created_screen_db.created_at,
            updated_at=created_screen_db.updated_at,
        )
        logger.info(f"Pantalla creada exitosamente: {response_screen.screen_id}")
        return response_screen

    async def get_screen(self, screen_id: str) -> Optional[ScreenResponse]:
        """Obtiene una pantalla por su ID."""
        db_screen = await self.screen_repo.get_by_id(screen_id)
        if not db_screen:
            return None
        return ScreenResponse(
            screen_id=db_screen.id,
            name=db_screen.name,
            location=db_screen.location,
            client_id=db_screen.client_id,
            status=db_screen.status,
            last_heartbeat=db_screen.last_heartbeat,
            created_at=db_screen.created_at,
            updated_at=db_screen.updated_at,
        )

    async def list_screens(self, client_id: str) -> List[ScreenResponse]:
        """Lista pantallas filtradas por cliente."""
        db_screens = await self.screen_repo.get_by_client_id(client_id)
        return [
            ScreenResponse(
                screen_id=s.id,
                name=s.name,
                location=s.location,
                client_id=s.client_id,
                status=s.status,
                last_heartbeat=s.last_heartbeat,
                created_at=s.created_at,
                updated_at=s.updated_at,
            )
            for s in db_screens
        ]

    # Otros métodos como update_screen, delete_screen irían aquí
    # async def update_screen(self, screen_id: str, update_data: ScreenUpdate) -> Optional[ScreenResponse]: ...
    # async def delete_screen(self, screen_id: str) -> bool: ...
    # async def update_screen_status(self, screen_id: str, status: ScreenStatus): ...
    # async def handle_heartbeat(self, screen_id: str): ...