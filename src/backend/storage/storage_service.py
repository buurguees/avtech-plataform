"""
AVTech Platform - Storage Service
=================================

High-level storage service for managing files and media.
"""

import os
import uuid
from typing import Optional, Dict, Any, BinaryIO
from pathlib import Path
from datetime import datetime

from src.backend.storage.minio_client import MinIOClient
from src.backend.monitoring.logger import get_logger
from src.backend.monitoring.metrics import record_storage_operation

logger = get_logger(__name__)


class StorageService:
    """High-level storage service for file management."""
    
    def __init__(self):
        self.minio_client = MinIOClient()
        self.base_path = "avtech-media"
    
    async def upload_video(
        self,
        file_path: str,
        client_id: str,
        title: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Upload a video file to storage.
        
        Args:
            file_path: Local file path
            client_id: Client ID
            title: Video title
            description: Video description
            
        Returns:
            Upload result with file info
        """
        try:
            # Generate unique object name
            file_extension = Path(file_path).suffix
            object_name = f"{self.base_path}/clients/{client_id}/videos/{uuid.uuid4()}{file_extension}"
            
            # Prepare metadata
            metadata = {
                "client_id": client_id,
                "title": title,
                "description": description or "",
                "upload_date": datetime.utcnow().isoformat(),
                "file_type": "video"
            }
            
            # Upload file
            result = await self.minio_client.upload_file(
                file_path=file_path,
                object_name=object_name,
                content_type="video/mp4",
                metadata=metadata
            )
            
            # Record metrics
            record_storage_operation(
                operation="upload_video",
                status="success",
                bytes_used=result["size"],
                bucket=self.minio_client.bucket_name
            )
            
            logger.info(f"Video uploaded successfully: {object_name}")
            
            return {
                "object_name": object_name,
                "file_path": result["file_path"],
                "size": result["size"],
                "hash_sha256": result["hash_sha256"],
                "content_type": result["content_type"],
                "metadata": metadata
            }
            
        except Exception as e:
            # Record error metrics
            record_storage_operation(
                operation="upload_video",
                status="error"
            )
            
            logger.error(f"Error uploading video: {e}")
            raise
    
    async def upload_thumbnail(
        self,
        file_path: str,
        client_id: str,
        video_id: str
    ) -> Dict[str, Any]:
        """
        Upload a video thumbnail to storage.
        
        Args:
            file_path: Local file path
            client_id: Client ID
            video_id: Video ID
            
        Returns:
            Upload result with file info
        """
        try:
            # Generate unique object name
            file_extension = Path(file_path).suffix
            object_name = f"{self.base_path}/clients/{client_id}/thumbnails/{video_id}{file_extension}"
            
            # Prepare metadata
            metadata = {
                "client_id": client_id,
                "video_id": video_id,
                "upload_date": datetime.utcnow().isoformat(),
                "file_type": "thumbnail"
            }
            
            # Upload file
            result = await self.minio_client.upload_file(
                file_path=file_path,
                object_name=object_name,
                content_type="image/jpeg",
                metadata=metadata
            )
            
            # Record metrics
            record_storage_operation(
                operation="upload_thumbnail",
                status="success",
                bytes_used=result["size"],
                bucket=self.minio_client.bucket_name
            )
            
            logger.info(f"Thumbnail uploaded successfully: {object_name}")
            
            return {
                "object_name": object_name,
                "file_path": result["file_path"],
                "size": result["size"],
                "hash_sha256": result["hash_sha256"],
                "content_type": result["content_type"],
                "metadata": metadata
            }
            
        except Exception as e:
            # Record error metrics
            record_storage_operation(
                operation="upload_thumbnail",
                status="error"
            )
            
            logger.error(f"Error uploading thumbnail: {e}")
            raise
    
    async def download_file(
        self,
        object_name: str,
        local_path: str
    ) -> bool:
        """
        Download a file from storage.
        
        Args:
            object_name: Object name in storage
            local_path: Local file path to save
            
        Returns:
            True if successful
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # Download file
            success = await self.minio_client.download_file(
                object_name=object_name,
                file_path=local_path
            )
            
            if success:
                # Record metrics
                record_storage_operation(
                    operation="download_file",
                    status="success"
                )
                
                logger.info(f"File downloaded successfully: {object_name}")
            else:
                # Record error metrics
                record_storage_operation(
                    operation="download_file",
                    status="error"
                )
            
            return success
            
        except Exception as e:
            # Record error metrics
            record_storage_operation(
                operation="download_file",
                status="error"
            )
            
            logger.error(f"Error downloading file: {e}")
            return False
    
    async def delete_file(self, object_name: str) -> bool:
        """
        Delete a file from storage.
        
        Args:
            object_name: Object name in storage
            
        Returns:
            True if successful
        """
        try:
            success = await self.minio_client.delete_file(object_name)
            
            if success:
                # Record metrics
                record_storage_operation(
                    operation="delete_file",
                    status="success"
                )
                
                logger.info(f"File deleted successfully: {object_name}")
            else:
                # Record error metrics
                record_storage_operation(
                    operation="delete_file",
                    status="error"
                )
            
            return success
            
        except Exception as e:
            # Record error metrics
            record_storage_operation(
                operation="delete_file",
                status="error"
            )
            
            logger.error(f"Error deleting file: {e}")
            return False
    
    async def get_file_info(self, object_name: str) -> Optional[Dict[str, Any]]:
        """
        Get file information from storage.
        
        Args:
            object_name: Object name in storage
            
        Returns:
            File info or None if not found
        """
        try:
            info = await self.minio_client.get_file_info(object_name)
            
            if info:
                # Record metrics
                record_storage_operation(
                    operation="get_file_info",
                    status="success"
                )
            else:
                # Record error metrics
                record_storage_operation(
                    operation="get_file_info",
                    status="error"
                )
            
            return info
            
        except Exception as e:
            # Record error metrics
            record_storage_operation(
                operation="get_file_info",
                status="error"
            )
            
            logger.error(f"Error getting file info: {e}")
            return None
    
    async def list_client_files(
        self,
        client_id: str,
        file_type: Optional[str] = None
    ) -> list:
        """
        List files for a specific client.
        
        Args:
            client_id: Client ID
            file_type: Optional file type filter (videos, thumbnails)
            
        Returns:
            List of file objects
        """
        try:
            prefix = f"{self.base_path}/clients/{client_id}/"
            if file_type:
                prefix += f"{file_type}/"
            
            files = await self.minio_client.list_files(prefix=prefix)
            
            # Record metrics
            record_storage_operation(
                operation="list_files",
                status="success"
            )
            
            return files
            
        except Exception as e:
            # Record error metrics
            record_storage_operation(
                operation="list_files",
                status="error"
            )
            
            logger.error(f"Error listing files: {e}")
            return []
    
    async def get_presigned_url(
        self,
        object_name: str,
        expires_in: int = 3600
    ) -> str:
        """
        Get a presigned URL for file access.
        
        Args:
            object_name: Object name in storage
            expires_in: URL expiration time in seconds
            
        Returns:
            Presigned URL
        """
        try:
            url = self.minio_client.get_presigned_url(
                object_name=object_name,
                expires_in=expires_in
            )
            
            # Record metrics
            record_storage_operation(
                operation="get_presigned_url",
                status="success"
            )
            
            return url
            
        except Exception as e:
            # Record error metrics
            record_storage_operation(
                operation="get_presigned_url",
                status="error"
            )
            
            logger.error(f"Error generating presigned URL: {e}")
            raise
    
    async def health_check(self) -> bool:
        """
        Check storage service health.
        
        Returns:
            True if healthy
        """
        try:
            return await self.minio_client.health_check()
        except Exception as e:
            logger.error(f"Storage health check failed: {e}")
            return False
