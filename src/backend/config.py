from pydantic_settings import BaseSettings
from typing import Optional
import os

class DatabaseSettings(BaseSettings):
    host: str = os.getenv("DB_HOST", "localhost")
    port: int = int(os.getenv("DB_PORT", 5432))
    user: str = os.getenv("DB_USER", "avtech_user")
    password: str = os.getenv("DB_PASSWORD", "avtech_password")
    database: str = os.getenv("DB_NAME", "avtech_db")
    echo: bool = os.getenv("DB_ECHO", "False").lower() == "true"

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

class StorageSettings(BaseSettings):
    endpoint: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    access_key: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    secret_key: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    secure: bool = os.getenv("MINIO_SECURE", "False").lower() == "true"
    bucket_name: str = os.getenv("MINIO_BUCKET_NAME", "avtech-media")

class RedisSettings(BaseSettings):
    host: str = os.getenv("REDIS_HOST", "localhost")
    port: int = int(os.getenv("REDIS_PORT", 6379))
    password: Optional[str] = os.getenv("REDIS_PASSWORD", None)

class ServerSettings(BaseSettings):
    host: str = os.getenv("SERVER_HOST", "0.0.0.0")
    port: int = int(os.getenv("SERVER_PORT", 8000))
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

class Settings(BaseSettings):
    database: DatabaseSettings = DatabaseSettings()
    storage: StorageSettings = StorageSettings()
    redis: RedisSettings = RedisSettings()
    server: ServerSettings = ServerSettings()

    class Config:
        env_file = ".env" # Carga variables desde .env si existe

# Instancia global de la configuración
settings = Settings()