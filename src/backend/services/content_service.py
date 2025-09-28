# src/backend/services/content_service.py
"""
Servicio de negocio para la gestión de contenido (videos).
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.database.models import VideoCreate, VideoResponse, VideoUpdate, VideoStatus
from src.backend.storage.storage_service import StorageService # Asumimos que se creará
from src.backend.exceptions.content_exceptions import VideoUploadException, StorageLimitExceededException
from src.backend.database.repository import VideoRepository # Asumimos que se creará
from src.backend.config import settings
import logging

logger = logging.getLogger(__name__)

class ContentService:
    def __init__(self, db_session: AsyncSession, storage_service: StorageService):
        self.db_session = db_session
        self.storage_service = storage_service
        self.video_repo = VideoRepository(db_session)

    async def upload_video(self, video_data: VideoCreate, file_data: bytes) -> VideoResponse:
        """
        Sube un video, lo valida (duración 1-20s), lo almacena y lo registra en la base de datos.
        """
        logger.info(f"Procesando subida de video: {video_data.title}")

        # --- Corrección Crítica 1: Validación de Duración ---
        # Aunque VideoCreate ya tiene validación Pydantic, la verificamos aquí por si acaso
        # y la aplicamos también si se recibe raw o se procesa.
        duration = video_data.duration_seconds
        if not (1 <= duration <= 20):
            raise VideoUploadException(f"La duración del video ({duration}s) no está entre 1 y 20 segundos.")

        # --- Corrección Crítica 2: Validación de Hash ---
        # Opcional: Verificar el hash del archivo recibido contra el proporcionado
        # Calculamos hash del file_data y lo comparamos con video_data.hash_sha256
        import hashlib
        calculated_hash = hashlib.sha256(file_data).hexdigest()
        if calculated_hash.lower() != video_data.hash_sha256.lower():
             raise VideoUploadException("El hash del archivo no coincide con el hash proporcionado.")

        # --- Corrección Crítica 3: Gestión de Almacenamiento ---
        # Verificar límite de almacenamiento del cliente (simulado aquí)
        # En un sistema real, esto se haría contra la base de datos o un servicio de límites
        client_storage_used = await self.get_client_storage_used(video_data.client_id)
        if client_storage_used + video_data.file_size_bytes > settings.client_storage_limit_bytes: # Asumimos que settings.client_storage_limit_bytes existe
             raise StorageLimitExceededException()

        # Almacenar el archivo en MinIO/S3
        try:
            storage_path = await self.storage_service.save_video(video_data.video_id, file_data)
        except Exception as e:
            logger.error(f"Error al almacenar video {video_data.video_id}: {e}")
            raise VideoUploadException(f"Error al almacenar el video: {str(e)}")

        # Crear el objeto Video para la base de datos
        # Aquí se asume que video_data no incluye video_id, que debe generarse
        # o se genera en el repositorio.
        # Tambien se asume que created_at, updated_at se manejan en la DB o aquí.
        from datetime import datetime
        db_video = {
            "title": video_data.title,
            "description": video_data.description,
            "duration_seconds": video_data.duration_seconds,
            "file_size_bytes": video_data.file_size_bytes,
            "hash_sha256": video_data.hash_sha256,
            "storage_path": storage_path, # Ruta donde se guardó
            "status": VideoStatus.PROCESSING, # O READY si no hay procesamiento adicional
            "client_id": video_data.client_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        # Guardar en la base de datos
        try:
            created_video_db = await self.video_repo.create(db_video)
        except Exception as e:
            logger.error(f"Error al guardar video {video_data.video_id} en DB: {e}")
            # Opcional: Eliminar el archivo subido si la DB falla
            try:
                await self.storage_service.delete_video(video_data.video_id)
            except:
                pass # No hacer nada si la eliminación falla
            raise VideoUploadException(f"Error al registrar el video: {str(e)}")

        # Convertir a VideoResponse
        response_video = VideoResponse(
            video_id=created_video_db.id, # Asumiendo que el modelo de DB tiene .id
            title=created_video_db.title,
            description=created_video_db.description,
            duration_seconds=created_video_db.duration_seconds,
            file_size_bytes=created_video_db.file_size_bytes,
            hash_sha256=created_video_db.hash_sha256,
            status=created_video_db.status,
            client_id=created_video_db.client_id,
            created_at=created_video_db.created_at,
            updated_at=created_video_db.updated_at,
        )
        logger.info(f"Video subido exitosamente: {response_video.video_id}")
        return response_video

    async def get_video(self, video_id: str) -> Optional[VideoResponse]:
        """Obtiene un video por su ID."""
        db_video = await self.video_repo.get_by_id(video_id)
        if not db_video:
            return None
        return VideoResponse(
            video_id=db_video.id,
            title=db_video.title,
            description=db_video.description,
            duration_seconds=db_video.duration_seconds,
            file_size_bytes=db_video.file_size_bytes,
            hash_sha256=db_video.hash_sha256,
            status=db_video.status,
            client_id=db_video.client_id,
            created_at=db_video.created_at,
            updated_at=db_video.updated_at,
        )

    async def list_videos(self, client_id: str) -> List[VideoResponse]:
        """Lista videos filtrados por cliente."""
        db_videos = await self.video_repo.get_by_client_id(client_id)
        return [
            VideoResponse(
                video_id=v.id,
                title=v.title,
                description=v.description,
                duration_seconds=v.duration_seconds,
                file_size_bytes=v.file_size_bytes,
                hash_sha256=v.hash_sha256,
                status=v.status,
                client_id=v.client_id,
                created_at=v.created_at,
                updated_at=v.updated_at,
            )
            for v in db_videos
        ]

    async def get_client_storage_used(self, client_id: str) -> int:
        """Obtiene el espacio de almacenamiento usado por un cliente."""
        # Simulación: En la realidad, esto sería una consulta a la base de datos
        # sumando los file_size_bytes de todos los videos del cliente.
        # O podría haber un servicio dedicado a límites/uso de almacenamiento.
        # Por ahora, devolvemos 0 para simplificar.
        # TODO: Implementar lógica real de cálculo de uso de almacenamiento
        return 0 # Placeholder

    # Otros métodos como update_video, delete_video irían aquí
    # async def update_video(self, video_id: str, update_data: VideoUpdate) -> Optional[VideoResponse]: ...
    # async def delete_video(self, video_id: str) -> bool: ...
