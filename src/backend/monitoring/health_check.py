"""
AVTech Platform - Health Check
==============================

Health check endpoints and monitoring for the AVTech Platform backend.
"""

import asyncio
import time
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.backend.database.connection import get_db_session
from src.backend.config import settings
import redis.asyncio as redis


class HealthChecker:
    """Health check manager for various services."""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self._last_checks: Dict[str, Dict[str, Any]] = {}
    
    async def check_database(self) -> Dict[str, Any]:
        """Check database connectivity and performance."""
        try:
            start_time = time.time()
            
            async with get_db_session() as session:
                # Simple query to test connectivity
                result = await session.execute(text("SELECT 1"))
                result.fetchone()
                
                response_time = time.time() - start_time
                
                return {
                    "status": "healthy",
                    "response_time_ms": round(response_time * 1000, 2),
                    "timestamp": datetime.utcnow().isoformat()
                }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def check_redis(self) -> Dict[str, Any]:
        """Check Redis connectivity and performance."""
        try:
            if not self.redis_client:
                self.redis_client = redis.Redis(
                    host=settings.redis.host,
                    port=settings.redis.port,
                    password=settings.redis.password,
                    decode_responses=True
                )
            
            start_time = time.time()
            
            # Test Redis connection
            await self.redis_client.ping()
            
            response_time = time.time() - start_time
            
            return {
                "status": "healthy",
                "response_time_ms": round(response_time * 1000, 2),
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def check_storage(self) -> Dict[str, Any]:
        """Check MinIO storage connectivity."""
        try:
            from src.backend.storage.minio_client import MinIOClient
            
            start_time = time.time()
            
            # Test MinIO connection
            client = MinIOClient()
            await client.health_check()
            
            response_time = time.time() - start_time
            
            return {
                "status": "healthy",
                "response_time_ms": round(response_time * 1000, 2),
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status."""
        checks = {
            "database": await self.check_database(),
            "redis": await self.check_redis(),
            "storage": await self.check_storage()
        }
        
        # Determine overall health
        all_healthy = all(
            check["status"] == "healthy" 
            for check in checks.values()
        )
        
        overall_status = "healthy" if all_healthy else "degraded"
        
        return {
            "status": overall_status,
            "timestamp": datetime.utcnow().isoformat(),
            "checks": checks,
            "version": "0.1.0",
            "service": "avtech-backend"
        }
    
    async def get_detailed_health(self) -> Dict[str, Any]:
        """Get detailed health information including metrics."""
        health = await self.get_system_health()
        
        # Add additional system information
        health.update({
            "uptime_seconds": time.time() - start_time if 'start_time' in globals() else 0,
            "environment": "development" if settings.server.debug else "production",
            "log_level": settings.server.log_level
        })
        
        return health


# Global health checker instance
health_checker = HealthChecker()


async def get_health() -> Dict[str, Any]:
    """Get basic health status."""
    return await health_checker.get_system_health()


async def get_detailed_health() -> Dict[str, Any]:
    """Get detailed health status."""
    return await health_checker.get_detailed_health()


async def get_readiness() -> Dict[str, Any]:
    """Get readiness status for Kubernetes."""
    health = await health_checker.get_system_health()
    
    if health["status"] == "healthy":
        return {"status": "ready"}
    else:
        raise HTTPException(
            status_code=503,
            detail="Service not ready"
        )


async def get_liveness() -> Dict[str, Any]:
    """Get liveness status for Kubernetes."""
    return {"status": "alive"}
