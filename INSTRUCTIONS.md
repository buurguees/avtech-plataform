# AVTech Platform - Guía de Implementación

## Tabla de Contenidos
1. [Configuración Inicial](#1-configuración-inicial)
2. [Entorno de Desarrollo](#2-entorno-de-desarrollo)
3. [Base de Datos](#3-base-de-datos)
4. [Backend](#4-backend)
5. [Frontend](#5-frontend)
6. [Player](#6-player)
7. [Testing](#7-testing)
8. [Deployment](#8-deployment)
9. [Plan de Trabajo](#9-plan-de-trabajo)

---

## 1. Configuración Inicial

### 1.1 Estructura del Proyecto

```bash
mkdir avtech-platform && cd avtech-platform

# Crear estructura de directorios
mkdir -p {backend,frontend,player,docs,scripts,tests,infra}
mkdir -p backend/{src,tests,migrations}
mkdir -p backend/src/{api,services,repositories,models,config,utils}
mkdir -p frontend/{apps,packages,shared}
mkdir -p player/{src,config,scripts,systemd}
mkdir -p infra/{docker,terraform,ansible}

# Inicializar Git
git init
git branch -M main
```

### 1.2 Variables de Entorno

Crear `.env`:

```bash
# Database
DATABASE_URL=postgresql://avtech_dev:dev_password@localhost:5432/avtech_dev

# Redis
REDIS_URL=redis://localhost:6379

# MinIO
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin123

# JWT
JWT_SECRET_KEY=your-super-secret-jwt-key-here
JWT_ALGORITHM=HS256

# App
DEBUG=true
ENVIRONMENT=development
```

---

## 2. Entorno de Desarrollo

### 2.1 Docker Compose

Crear `docker-compose.dev.yml`:

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: avtech_dev
      POSTGRES_USER: avtech_dev
      POSTGRES_PASSWORD: dev_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin123

volumes:
  postgres_data:
```

### 2.2 Script de Setup

Crear `scripts/setup-dev.sh`:

```bash
#!/bin/bash
set -e

echo "Configurando entorno de desarrollo..."

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "Error: Docker no está instalado"
    exit 1
fi

# Iniciar servicios
docker-compose -f docker-compose.dev.yml up -d

# Esperar PostgreSQL
until docker exec avtech-postgres-dev pg_isready -U avtech_dev; do
  sleep 2
done

# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install

echo "Entorno configurado exitosamente"
```

---

## 3. Base de Datos

### 3.1 Migración Inicial

Crear `backend/migrations/001_initial.sql`:

```sql
-- Esquemas
CREATE SCHEMA IF NOT EXISTS admin;
CREATE SCHEMA IF NOT EXISTS core;
CREATE SCHEMA IF NOT EXISTS user_views;

-- Extensiones
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Función para updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Tabla de clientes
CREATE TABLE admin.clients (
    client_id TEXT PRIMARY KEY DEFAULT 'CLI-' || to_char(now(), 'YYYYMMDD') || '-' || lpad(nextval('serial')::text, 5, '0'),
    name VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255) NOT NULL,
    max_screens INTEGER DEFAULT 10,
    max_storage_gb INTEGER DEFAULT 10,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla de videos (CORREGIDA)
CREATE TABLE core.videos (
    video_id TEXT PRIMARY KEY DEFAULT 'VID-' || to_char(now(), 'YYYYMMDD') || '-' || lpad(nextval('serial')::text, 5, '0'),
    client_id TEXT NOT NULL REFERENCES admin.clients(client_id),
    filename VARCHAR(255) NOT NULL,
    original_name VARCHAR(255),
    duration_seconds INTEGER NOT NULL CHECK (duration_seconds > 0 AND duration_seconds <= 20),
    file_size_bytes BIGINT NOT NULL,
    hash_sha256 TEXT UNIQUE NOT NULL,
    storage_path TEXT NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Triggers
CREATE TRIGGER update_clients_updated_at 
    BEFORE UPDATE ON admin.clients 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_videos_updated_at 
    BEFORE UPDATE ON core.videos 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Índices
CREATE INDEX idx_videos_client ON core.videos(client_id);
CREATE INDEX idx_videos_duration ON core.videos(duration_seconds);
CREATE INDEX idx_videos_hash ON core.videos(hash_sha256);
```

### 3.2 Script de Migración

Crear `backend/migrate.py`:

```python
#!/usr/bin/env python3
import asyncio
import asyncpg
import os
from pathlib import Path

async def run_migrations():
    database_url = os.getenv('DATABASE_URL')
    connection = await asyncpg.connect(database_url)
    
    try:
        migrations_dir = Path('migrations')
        for migration_file in sorted(migrations_dir.glob('*.sql')):
            print(f"Ejecutando: {migration_file.name}")
            with open(migration_file, 'r') as f:
                await connection.execute(f.read())
            print(f"Completado: {migration_file.name}")
    finally:
        await connection.close()

if __name__ == '__main__':
    asyncio.run(run_migrations())
```

---

## 4. Backend

### 4.1 Dependencias

Crear `backend/requirements.txt`:

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
asyncpg==0.29.0
pydantic==2.5.0
pydantic-settings==2.1.0
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0
python-multipart==0.0.6
celery==5.3.4
redis==5.0.1
ffmpeg-python==0.2.0
python-magic==0.4.27
httpx==0.25.2
structlog==23.2.0
python-dotenv==1.0.0

# Dev dependencies
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.11.0
```

### 4.2 Configuración

Crear `backend/src/config/settings.py`:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    
    # MinIO
    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    
    # Limits
    max_video_size: int = 100 * 1024 * 1024  # 100MB
    max_video_duration: int = 20  # seconds
    
    debug: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### 4.3 Aplicación Principal

Crear `backend/src/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.config.settings import settings
from src.models.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    pass

app = FastAPI(
    title="AVTech Platform API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else ["https://admin.avtech.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.debug)
```

### 4.4 Servicio de Contenido (con correcciones)

Crear `backend/src/services/content_service.py`:

```python
import hashlib
import ffmpeg
from typing import Optional

class ContentService:
    async def upload_video(self, file_data: bytes, filename: str, client_id: str) -> dict:
        # 1. Validar duración (CORREGIDO: 1-20 segundos)
        duration = await self.get_video_duration(file_data)
        if duration <= 0 or duration > 20:
            raise ValueError("Video debe durar entre 1 y 20 segundos")
        
        # 2. Calcular hash
        file_hash = hashlib.sha256(file_data).hexdigest()
        
        # 3. Verificar duplicados
        existing = await self.check_existing_video(file_hash)
        if existing:
            return existing
        
        # 4. Almacenar archivo
        storage_path = await self.store_file(file_data, file_hash)
        
        # 5. Crear registro
        video_data = {
            "client_id": client_id,
            "filename": filename,
            "duration_seconds": duration,
            "file_size_bytes": len(file_data),
            "hash_sha256": file_hash,
            "storage_path": storage_path
        }
        
        return await self.create_video_record(video_data)
    
    async def get_video_duration(self, file_data: bytes) -> int:
        # Usar ffprobe para obtener duración real
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file_data)
            tmp.flush()
            
            try:
                probe = ffmpeg.probe(tmp.name)
                duration = float(probe['streams'][0]['duration'])
                return int(duration)
            finally:
                os.unlink(tmp.name)
```

### 4.5 Script de Desarrollo

Crear `backend/run-dev.sh`:

```bash
#!/bin/bash
set -e

echo "Iniciando backend..."

# Activar entorno virtual
source venv/bin/activate

# Cargar variables de entorno
set -a
source ../.env
set +a

# Ejecutar migraciones
python migrate.py

# Iniciar servidor
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 5. Frontend

### 5.1 Configuración Next.js

Crear `frontend/package.json`:

```json
{
  "name": "avtech-frontend",
  "version": "1.0.0",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "@tanstack/react-query": "^5.0.0",
    "axios": "^1.6.0",
    "react-hook-form": "^7.48.0",
    "zod": "^3.22.0",
    "lucide-react": "^0.294.0",
    "tailwindcss": "^3.3.0"
  }
}
```

### 5.2 Componente de Upload (con validación corregida)

Crear `frontend/src/components/video-uploader.tsx`:

```tsx
import React, { useState } from 'react';
import { Upload, AlertCircle } from 'lucide-react';

export function VideoUploader() {
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);

  const validateVideo = (file: File): Promise<number> => {
    return new Promise((resolve, reject) => {
      const video = document.createElement('video');
      video.src = URL.createObjectURL(file);
      
      video.onloadedmetadata = () => {
        const duration = Math.ceil(video.duration);
        URL.revokeObjectURL(video.src);
        
        // CORREGIDO: Validar rango 1-20 segundos
        if (duration <= 0 || duration > 20) {
          reject(new Error(`Duración inválida: ${duration}s. Debe ser entre 1-20 segundos`));
        } else {
          resolve(duration);
        }
      };
    });
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (!selectedFile) return;

    setError(null);

    // Validar tipo
    if (!selectedFile.type.startsWith('video/')) {
      setError('Selecciona un archivo de video');
      return;
    }

    // Validar tamaño
    if (selectedFile.size > 100 * 1024 * 1024) {
      setError('Archivo muy grande (máximo 100MB)');
      return;
    }

    try {
      const duration = await validateVideo(selectedFile);
      setFile(selectedFile);
      console.log(`Video válido: ${duration} segundos`);
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div className="border-2 border-dashed p-8 text-center">
      <input
        type="file"
        accept="video/*"
        onChange={handleFileChange}
        className="hidden"
        id="video-upload"
      />
      
      <label htmlFor="video-upload" className="cursor-pointer">
        <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
        <p>Subir video (1-20 segundos, máximo 100MB)</p>
      </label>

      {error && (
        <div className="mt-4 p-3 bg-red-50 text-red-700 rounded flex items-center">
          <AlertCircle className="h-4 w-4 mr-2" />
          {error}
        </div>
      )}

      {file && (
        <div className="mt-4">
          <video src={URL.createObjectURL(file)} controls className="max-h-64" />
          <p className="text-sm text-gray-600 mt-2">{file.name}</p>
        </div>
      )}
    </div>
  );
}
```

---

## 6. Player

### 6.1 Configuración del Player

Crear `player/config.yaml`:

```yaml
screen_code: "SCR-EXAMPLE-001"
client_id: "CLI-EXAMPLE-001"
api_key: "player-api-key-here"

server:
  base_url: "http://server:8080"
  
storage:
  root: "/opt/avtech/media"
  min_free_gb: 5
  retention_days: 30

sync:
  interval: 60
  max_retries: 3
```

### 6.2 Reconciler Robusto

Crear `player/src/reconciler.py`:

```python
import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class Reconciler:
    def __init__(self, config):
        self.config = config
        self.consecutive_failures = 0
        self.last_applied_version = 0

    async def reconcile(self) -> bool:
        """Proceso de reconciliación con manejo de errores"""
        try:
            # 1. Verificar conectividad
            if not await self.check_server_connection():
                logger.warning("Sin conexión al servidor")
                return False

            # 2. Obtener estado deseado
            desired_state = await self.fetch_desired_state()
            if not desired_state:
                return False

            # 3. Verificar cambios
            if desired_state['version'] <= self.last_applied_version:
                return True

            # 4. Aplicar cambios atómicamente
            success = await self.apply_state_atomically(desired_state)
            
            if success:
                self.last_applied_version = desired_state['version']
                self.consecutive_failures = 0
                logger.info(f"Reconciliación exitosa versión {desired_state['version']}")
                return True
            else:
                raise Exception("Falló aplicación de estado")

        except Exception as e:
            self.consecutive_failures += 1
            logger.error(f"Reconciliación falló: {e}")
            
            # Backoff exponencial
            backoff = min(60 * self.consecutive_failures, 300)
            await asyncio.sleep(backoff)
            return False

    async def apply_state_atomically(self, desired_state: Dict[str, Any]) -> bool:
        """Aplica estado de forma atómica con rollback"""
        try:
            video_ids = desired_state['video_ids']
            
            # 1. Descargar videos faltantes
            missing = await self.identify_missing_videos(video_ids)
            for video_id in missing:
                success = await self.download_video(video_id)
                if not success:
                    logger.error(f"Falló descarga: {video_id}")
                    return False

            # 2. Aplicar playlist
            success = await self.apply_playlist(video_ids)
            if not success:
                await self.rollback_playlist()
                return False

            return True

        except Exception as e:
            logger.error(f"Error en aplicación atómica: {e}")
            await self.rollback_playlist()
            return False

    async def download_video(self, video_id: str) -> bool:
        """Descarga video con verificación de integridad"""
        try:
            # Obtener URL de descarga
            download_info = await self.get_download_info(video_id)
            if not download_info:
                return False

            # Descargar y verificar hash
            file_data = await self.download_file(download_info['url'])
            actual_hash = hashlib.sha256(file_data).hexdigest()
            
            if actual_hash != download_info['hash']:
                logger.error(f"Hash mismatch para {video_id}")
                return False

            # Almacenar archivo
            await self.store_video_file(video_id, file_data)
            return True

        except Exception as e:
            logger.error(f"Error descargando {video_id}: {e}")
            return False
```

### 6.3 Script de Instalación

Crear `player/scripts/install.sh`:

```bash
#!/bin/bash
set -e

echo "Instalando AVTech Player..."

# Verificar root
if [[ $EUID -ne 0 ]]; then
    echo "Debe ejecutarse como root"
    exit 1
fi

# Instalar dependencias
apt update
apt install -y python3 python3-pip python3-venv ffmpeg systemd

# Crear directorios
mkdir -p /opt/avtech-player
mkdir -p /etc/avtech
mkdir -p /var/log/avtech

# Crear usuario
useradd -r -s /bin/false avtech

# Copiar archivos
cp -r . /opt/avtech-player/
chown -R avtech:avtech /opt/avtech-player

# Instalar dependencias Python
cd /opt/avtech-player
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configurar systemd
cat > /etc/systemd/system/avtech-player.service << EOF
[Unit]
Description=AVTech Player
After=network.target

[Service]
Type=simple
User=avtech
WorkingDirectory=/opt/avtech-player
ExecStart=/opt/avtech-player/venv/bin/python src/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Habilitar servicio
systemctl daemon-reload
systemctl enable avtech-player

echo "Instalación completada"
```

---

## 7. Testing

### 7.1 Tests de Backend

Crear `backend/tests/test_content_service.py`:

```python
import pytest
from unittest.mock import AsyncMock, patch
from src.services.content_service import ContentService

class TestContentService:
    
    @pytest.fixture
    def content_service(self):
        return ContentService()

    async def test_video_duration_validation_corrected(self, content_service):
        """Test validación de duración corregida (1-20 segundos)"""
        
        # Video de 15 segundos - debe ser válido
        with patch.object(content_service, 'get_video_duration', return_value=15):
            result = await content_service.upload_video(
                b"video_data", "test.mp4", "CLI-TEST-001"
            )
            assert result is not None

        # Video de 25 segundos - debe fallar
        with patch.object(content_service, 'get_video_duration', return_value=25):
            with pytest.raises(ValueError, match="entre 1 y 20 segundos"):
                await content_service.upload_video(
                    b"video_data", "test.mp4", "CLI-TEST-001"
                )

        # Video de 0 segundos - debe fallar
        with patch.object(content_service, 'get_video_duration', return_value=0):
            with pytest.raises(ValueError, match="entre 1 y 20 segundos"):
                await content_service.upload_video(
                    b"video_data", "test.mp4", "CLI-TEST-001"
                )

    async def test_video_duration_edge_cases(self, content_service):
        """Test casos límite de duración"""
        
        # 1 segundo - debe ser válido
        with patch.object(content_service, 'get_video_duration', return_value=1):
            result = await content_service.upload_video(
                b"video_data", "test.mp4", "CLI-TEST-001"
            )
            assert result is not None

        # 20 segundos - debe ser válido
        with patch.object(content_service, 'get_video_duration', return_value=20):
            result = await content_service.upload_video(
                b"video_data", "test.mp4", "CLI-TEST-001"
            )
            assert result is not None

        # 21 segundos - debe fallar
        with patch.object(content_service, 'get_video_duration', return_value=21):
            with pytest.raises(ValueError):
                await content_service.upload_video(
                    b"video_data", "test.mp4", "CLI-TEST-001"
                )
```

### 7.2 Tests de Player

Crear `player/tests/test_reconciler.py`:

```python
import pytest
from unittest.mock import AsyncMock, MagicMock
from src.reconciler import Reconciler

class TestReconciler:
    
    @pytest.fixture
    def reconciler(self):
        config = MagicMock()
        return Reconciler(config)

    async def test_reconciliation_with_network_error(self, reconciler):
        """Test reconciliación con error de red"""
        
        # Simular error de conexión
        reconciler.check_server_connection = AsyncMock(return_value=False)
        
        result = await reconciler.reconcile()
        
        assert result is False

    async def test_reconciliation_with_download_failure(self, reconciler):
        """Test reconciliación con fallo de descarga"""
        
        reconciler.check_server_connection = AsyncMock(return_value=True)
        reconciler.fetch_desired_state = AsyncMock(return_value={
            'version': 2,
            'video_ids': ['VID-TEST-001']
        })
        reconciler.identify_missing_videos = AsyncMock(return_value=['VID-TEST-001'])
        reconciler.download_video = AsyncMock(return_value=False)  # Falla descarga
        
        result = await reconciler.reconcile()
        
        assert result is False

    async def test_atomic_rollback_on_failure(self, reconciler):
        """Test rollback automático en fallos"""
        
        reconciler.apply_playlist = AsyncMock(return_value=False)  # Falla aplicación
        reconciler.rollback_playlist = AsyncMock()
        
        result = await reconciler.apply_state_atomically({
            'video_ids': ['VID-TEST-001']
        })
        
        assert result is False
        reconciler.rollback_playlist.assert_called_once()
```

---

## 8. Deployment

### 8.1 Docker para Producción

Crear `Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario
RUN useradd --create-home --shell /bin/bash app

WORKDIR /app

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .
RUN chown -R app:app /app

USER app
EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 8.2 Script de Deploy

Crear `scripts/deploy.sh`:

```bash
#!/bin/bash
set -e

VERSION=${1:-"latest"}
ENV=${2:-"production"}

echo "Desplegando AVTech Platform v$VERSION en $ENV"

# Backup de base de datos
echo "Creando backup..."
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql

# Construir imágenes
docker build -t avtech-backend:$VERSION ./backend
docker build -t avtech-frontend:$VERSION ./frontend

# Ejecutar migraciones
echo "Ejecutando migraciones..."
docker run --rm --network host avtech-backend:$VERSION python migrate.py

# Desplegar servicios
docker-compose -f docker-compose.prod.yml up -d

# Verificar salud
sleep 30
curl -f http://localhost:8000/health || exit 1

echo "Despliegue completado exitosamente"
```

---

## 9. Plan de Trabajo

### Semana 1: Configuración e Infraestructura
**Días 1-2:**
- Configurar estructura del proyecto
- Configurar Docker y entorno de desarrollo
- Configurar base de datos con migraciones corregidas

**Días 3-5:**
- Implementar backend básico (FastAPI + SQLAlchemy)
- Implementar APIs fundamentales (auth, upload con validación corregida)
- Testing básico de endpoints

### Semana 2: Backend Core
**Días 1-3:**
- Implementar servicios de contenido con gestión de almacenamiento
- Implementar publisher service con manejo de concurrencia
- Implementar storage service con limpieza automática

**Días 4-5:**
- Implementar observabilidad y métricas
- Testing de servicios con escenarios de fallo
- Documentación de APIs

### Semana 3: Player y Reconciliación
**Días 1-3:**
- Implementar player básico con reconciler robusto
- Implementar storage manager local
- Implementar network manager con retry

**Días 4-5:**
- Testing de player con simulación de fallos
- Scripts de provisioning básico
- Integración player-backend

### Semana 4: Frontend
**Días 1-3:**
- Configurar Next.js con componentes básicos
- Implementar upload component con validación corregida
- Implementar dashboard de pantallas

**Días 4-5:**
- Implementar programación de contenido
- Testing frontend con Playwright
- Integración frontend-backend

### Semana 5: Testing e Integración
**Días 1-3:**
- Testing de integración completo
- Testing de escenarios de fallo críticos
- Performance testing básico

**Días 4-5:**
- Documentación completa
- Scripts de deployment
- Preparación para producción

### Semana 6: Deployment y Monitoreo
**Días 1-3:**
- Configuración de producción
- Implementación de monitoreo
- Deployment inicial

**Días 4-5:**
- Pruebas en producción
- Ajustes finales
- Documentación de operación

---

## Comandos de Inicio Rápido

```bash
# Configurar proyecto
git clone <repo>
cd avtech-platform
chmod +x scripts/setup-dev.sh
./scripts/setup-dev.sh

# Iniciar desarrollo backend
cd backend
./run-dev.sh

# Iniciar desarrollo frontend (terminal separado)
cd frontend
npm run dev

# Ejecutar tests
cd backend
pytest

# Deploy a producción
./scripts/deploy.sh v1.0.0 production
```

Este plan proporciona una hoja de ruta clara y detallada para implementar el proyecto AVTech con todas las correcciones críticas incluidas. Cada semana tiene objetivos específicos y al final tendrás un sistema robusto y listo para producción.