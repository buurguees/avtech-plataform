# src/backend/services/schedule_service.py
"""
Servicio de negocio para la gestión de programación de contenido.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.database.models import (
    ScheduleRuleCreate, ScheduleRuleResponse, ScheduleRuleUpdate,
    TimeSlot, ActivePlaylist, ActiveVideo # Asumiendo que ActivePlaylist/ActiveVideo estén en models
)
from src.backend.database.repository import ScheduleRuleRepository # Asumimos que se creará
from src.backend.exceptions.validation_exceptions import ScheduleValidationException # Asumimos que se creará
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ScheduleService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.schedule_repo = ScheduleRuleRepository(db_session)

    async def create_schedule_rule(self, rule_data: ScheduleRuleCreate) -> ScheduleRuleResponse:
        """Crea una nueva regla de programación."""
        logger.info(f"Creando regla de programación: {rule_data.name}")
        # Validar regla (horarios, conflictos, etc.) - Pendiente de implementar
        # await self._validate_schedule_rule(rule_data)

        # Tambien se asume que created_at, updated_at se manejan en la DB o aquí.
        db_rule = {
            "name": rule_data.name,
            "rule_type": rule_data.rule_type,
            "active_from": rule_data.active_from,
            "active_until": rule_data.active_until,
            "time_slots": [ts.dict() for ts in rule_data.time_slots], # Serializar TimeSlot
            "client_id": rule_data.client_id,
            "screen_ids": rule_data.screen_ids,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        try:
            created_rule_db = await self.schedule_repo.create(db_rule)
        except Exception as e:
            logger.error(f"Error al crear regla de programación {rule_data.name}: {e}")
            raise ScheduleValidationException(f"Error al registrar la regla de programación: {str(e)}")

        response_rule = ScheduleRuleResponse(
            rule_id=created_rule_db.id,
            name=created_rule_db.name,
            rule_type=created_rule_db.rule_type,
            active_from=created_rule_db.active_from,
            active_until=created_rule_db.active_until,
            time_slots=[TimeSlot(**ts) for ts in created_rule_db.time_slots], # Deserializar TimeSlot
            client_id=created_rule_db.client_id,
            screen_ids=created_rule_db.screen_ids,
            created_at=created_rule_db.created_at,
            updated_at=created_rule_db.updated_at,
        )
        logger.info(f"Regla de programación creada exitosamente: {response_rule.rule_id}")
        return response_rule

    async def get_schedule_rule(self, rule_id: str) -> Optional[ScheduleRuleResponse]:
        """Obtiene una regla de programación por su ID."""
        db_rule = await self.schedule_repo.get_by_id(rule_id)
        if not db_rule:
            return None
        return ScheduleRuleResponse(
            rule_id=db_rule.id,
            name=db_rule.name,
            rule_type=db_rule.rule_type,
            active_from=db_rule.active_from,
            active_until=db_rule.active_until,
            time_slots=[TimeSlot(**ts) for ts in db_rule.time_slots],
            client_id=db_rule.client_id,
            screen_ids=db_rule.screen_ids,
            created_at=db_rule.created_at,
            updated_at=db_rule.updated_at,
        )

    async def list_schedule_rules(self, client_id: str) -> List[ScheduleRuleResponse]:
        """Lista reglas de programación filtradas por cliente."""
        db_rules = await self.schedule_repo.get_by_client_id(client_id)
        return [
            ScheduleRuleResponse(
                rule_id=r.id,
                name=r.name,
                rule_type=r.rule_type,
                active_from=r.active_from,
                active_until=r.active_until,
                time_slots=[TimeSlot(**ts) for ts in r.time_slots],
                client_id=r.client_id,
                screen_ids=r.screen_ids,
                created_at=r.created_at,
                updated_at=r.updated_at,
            )
            for r in db_rules
        ]

    # async def _validate_schedule_rule(self, rule_data: ScheduleRuleCreate):
    #     # Lógica de validación de horarios y conflictos
    #     # Pendiente de implementar según validation.py
    #     pass

    # async def resolve_schedule_for_screen(self, screen_id: str, timestamp: datetime) -> ActivePlaylist:
    #     # Lógica para resolver las reglas activas a una playlist específica
    #     # Pendiente de implementar según resolver.py
    #     pass

    # Otros métodos como update_schedule_rule, delete_schedule_rule irían aquí
    # async def update_schedule_rule(self, rule_id: str, update_data: ScheduleRuleUpdate) -> Optional[ScheduleRuleResponse]: ...
    # async def delete_schedule_rule(self, rule_id: str) -> bool: ...