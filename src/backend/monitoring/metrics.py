"""
AVTech Platform - Metrics Configuration
======================================

Prometheus metrics configuration for the AVTech Platform backend.
"""

from prometheus_client import Counter, Histogram, Gauge, Info, generate_latest
from typing import Dict, Any


# Application Info
app_info = Info('avtech_app_info', 'Application information')
app_info.info({
    'version': '0.1.0',
    'service': 'avtech-backend',
    'description': 'AVTech Platform Backend API'
})

# HTTP Metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

# Database Metrics
db_connections_active = Gauge(
    'db_connections_active',
    'Active database connections'
)

db_query_duration_seconds = Histogram(
    'db_query_duration_seconds',
    'Database query duration in seconds',
    ['query_type']
)

# Storage Metrics
storage_operations_total = Counter(
    'storage_operations_total',
    'Total storage operations',
    ['operation', 'status']
)

storage_bytes_total = Gauge(
    'storage_bytes_total',
    'Total storage usage in bytes',
    ['bucket']
)

# Video Processing Metrics
video_uploads_total = Counter(
    'video_uploads_total',
    'Total video uploads',
    ['status']
)

video_processing_duration_seconds = Histogram(
    'video_processing_duration_seconds',
    'Video processing duration in seconds'
)

# Screen Management Metrics
screens_online = Gauge(
    'screens_online',
    'Number of online screens'
)

screens_total = Gauge(
    'screens_total',
    'Total number of screens'
)

# Sync Metrics
sync_operations_total = Counter(
    'sync_operations_total',
    'Total sync operations',
    ['screen_id', 'status']
)

sync_duration_seconds = Histogram(
    'sync_duration_seconds',
    'Sync operation duration in seconds',
    ['screen_id']
)

# Error Metrics
errors_total = Counter(
    'errors_total',
    'Total errors',
    ['error_type', 'component']
)

# Custom Metrics
def get_metrics() -> str:
    """Get all metrics in Prometheus format."""
    return generate_latest()


def record_http_request(method: str, endpoint: str, status_code: int, duration: float):
    """Record HTTP request metrics."""
    http_requests_total.labels(
        method=method,
        endpoint=endpoint,
        status_code=str(status_code)
    ).inc()
    
    http_request_duration_seconds.labels(
        method=method,
        endpoint=endpoint
    ).observe(duration)


def record_db_query(query_type: str, duration: float):
    """Record database query metrics."""
    db_query_duration_seconds.labels(query_type=query_type).observe(duration)


def record_storage_operation(operation: str, status: str, bytes_used: int = 0, bucket: str = ""):
    """Record storage operation metrics."""
    storage_operations_total.labels(
        operation=operation,
        status=status
    ).inc()
    
    if bytes_used > 0 and bucket:
        storage_bytes_total.labels(bucket=bucket).set(bytes_used)


def record_video_upload(status: str, duration: float = 0):
    """Record video upload metrics."""
    video_uploads_total.labels(status=status).inc()
    
    if duration > 0:
        video_processing_duration_seconds.observe(duration)


def record_screen_status(online_count: int, total_count: int):
    """Record screen status metrics."""
    screens_online.set(online_count)
    screens_total.set(total_count)


def record_sync_operation(screen_id: str, status: str, duration: float = 0):
    """Record sync operation metrics."""
    sync_operations_total.labels(
        screen_id=screen_id,
        status=status
    ).inc()
    
    if duration > 0:
        sync_duration_seconds.labels(screen_id=screen_id).observe(duration)


def record_error(error_type: str, component: str):
    """Record error metrics."""
    errors_total.labels(
        error_type=error_type,
        component=component
    ).inc()
