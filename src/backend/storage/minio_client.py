"""
AVTech Platform - MinIO Client
==============================

MinIO client for object storage operations.
"""

import asyncio
from typing import Optional, BinaryIO, Dict, Any
from minio import Minio
from minio.error import S3Error
import aiofiles
import hashlib
import os
from pathlib import Path

from src.backend.config import settings
from src.backend.monitoring.logger import get_logger

logger = get_logger(__name__)


class MinIOClient:
    """MinIO client for storage operations."""
    
    def __init__(self):
        self.client = Minio(
            endpoint=settings.storage.endpoint,
            access_key=settings.storage.access_key,
            secret_key=settings.storage.secret_key,
            secure=settings.storage.secure
        )
        self.bucket_name = settings.storage.bucket_name
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """Ensure the bucket exists, create if it doesn't."""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"Created bucket: {self.bucket_name}")
        except S3Error as e:
            logger.error(f"Error creating bucket: {e}")
            raise
    
    async def upload_file(
        self,
        file_path: str,
        object_name: str,
        content_type: str = "application/octet-stream",
        metadata: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Upload a file to MinIO.
        
        Args:
            file_path: Local file path
            object_name: Object name in bucket
            content_type: MIME type
            metadata: Optional metadata
            
        Returns:
            Upload result with file info
        """
        try:
            # Calculate file hash
            file_hash = await self._calculate_file_hash(file_path)
            
            # Prepare metadata
            if metadata is None:
                metadata = {}
            metadata["sha256"] = file_hash
            
            # Upload file
            result = self.client.fput_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                file_path=file_path,
                content_type=content_type,
                metadata=metadata
            )
            
            logger.info(f"File uploaded successfully: {object_name}")
            
            return {
                "object_name": object_name,
                "etag": result.etag,
                "size": result.size,
                "hash_sha256": file_hash,
                "content_type": content_type
            }
            
        except S3Error as e:
            logger.error(f"Error uploading file {object_name}: {e}")
            raise
    
    async def download_file(
        self,
        object_name: str,
        file_path: str
    ) -> bool:
        """
        Download a file from MinIO.
        
        Args:
            object_name: Object name in bucket
            file_path: Local file path to save
            
        Returns:
            True if successful
        """
        try:
            self.client.fget_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                file_path=file_path
            )
            
            logger.info(f"File downloaded successfully: {object_name}")
            return True
            
        except S3Error as e:
            logger.error(f"Error downloading file {object_name}: {e}")
            return False
    
    async def delete_file(self, object_name: str) -> bool:
        """
        Delete a file from MinIO.
        
        Args:
            object_name: Object name in bucket
            
        Returns:
            True if successful
        """
        try:
            self.client.remove_object(
                bucket_name=self.bucket_name,
                object_name=object_name
            )
            
            logger.info(f"File deleted successfully: {object_name}")
            return True
            
        except S3Error as e:
            logger.error(f"Error deleting file {object_name}: {e}")
            return False
    
    async def get_file_info(self, object_name: str) -> Optional[Dict[str, Any]]:
        """
        Get file information from MinIO.
        
        Args:
            object_name: Object name in bucket
            
        Returns:
            File info or None if not found
        """
        try:
            stat = self.client.stat_object(
                bucket_name=self.bucket_name,
                object_name=object_name
            )
            
            return {
                "object_name": object_name,
                "size": stat.size,
                "etag": stat.etag,
                "content_type": stat.content_type,
                "last_modified": stat.last_modified,
                "metadata": stat.metadata
            }
            
        except S3Error as e:
            logger.error(f"Error getting file info {object_name}: {e}")
            return None
    
    async def list_files(
        self,
        prefix: str = "",
        recursive: bool = True
    ) -> list:
        """
        List files in the bucket.
        
        Args:
            prefix: Object name prefix
            recursive: Whether to list recursively
            
        Returns:
            List of file objects
        """
        try:
            objects = self.client.list_objects(
                bucket_name=self.bucket_name,
                prefix=prefix,
                recursive=recursive
            )
            
            files = []
            for obj in objects:
                files.append({
                    "object_name": obj.object_name,
                    "size": obj.size,
                    "etag": obj.etag,
                    "last_modified": obj.last_modified
                })
            
            return files
            
        except S3Error as e:
            logger.error(f"Error listing files: {e}")
            return []
    
    async def health_check(self) -> bool:
        """
        Check MinIO service health.
        
        Returns:
            True if healthy
        """
        try:
            # Try to list buckets
            self.client.list_buckets()
            return True
        except S3Error as e:
            logger.error(f"MinIO health check failed: {e}")
            return False
    
    async def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA256 hash of a file."""
        hash_sha256 = hashlib.sha256()
        
        async with aiofiles.open(file_path, "rb") as f:
            while chunk := await f.read(8192):
                hash_sha256.update(chunk)
        
        return hash_sha256.hexdigest()
    
    def get_presigned_url(
        self,
        object_name: str,
        expires_in: int = 3600
    ) -> str:
        """
        Get a presigned URL for file access.
        
        Args:
            object_name: Object name in bucket
            expires_in: URL expiration time in seconds
            
        Returns:
            Presigned URL
        """
        try:
            url = self.client.presigned_get_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                expires=expires_in
            )
            return url
        except S3Error as e:
            logger.error(f"Error generating presigned URL: {e}")
            raise
