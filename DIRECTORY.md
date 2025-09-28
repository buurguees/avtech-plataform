# AVTech Platform - Estructura Detallada de Directorios

## 🚀 Backend (`/backend`) - Aplicación Principal del Servidor

### **Estructura General**
```
backend/
├── .env                          # Variables de entorno específicas del backend
├── .env.example                  # Plantilla para configuración
├── requirements.txt              # Dependencias principales de producción
├── requirements-dev.txt          # Dependencias adicionales para desarrollo
├── Dockerfile                    # Imagen Docker para producción
├── docker-compose.override.yml   # Override para desarrollo con hot-reload
├── run-dev.sh                   # Script de inicio para desarrollo
├── migrate.py                   # Script principal de migraciones
├── alembic.ini                  # Configuración de Alembic (futuro)
└── pyproject.toml               # Configuración moderna de Python
```

### **`src/` - Código Fuente Principal**

#### **`src/api/` - Endpoints y Rutas de la API**
```
api/
├── __init__.py
├── dependencies.py              # Dependencias compartidas (autenticación, DB, etc.)
├── middleware.py               # Registro de middleware personalizado
│
├── v1/                         # Versión 1 de la API (versionado futuro)
│   ├── __init__.py
│   ├── router.py               # Router principal que agrupa todas las rutas
│   │
│   ├── auth/                   # 🔐 Autenticación y Autorización
│   │   ├── __init__.py
│   │   ├── routes.py           # POST /login, /refresh, /logout
│   │   ├── dependencies.py     # get_current_user, require_admin, etc.
│   │   └── schemas.py          # LoginRequest, TokenResponse, UserInfo
│   │
│   ├── content/                # 📹 Gestión de Contenido y Videos
│   │   ├── __init__.py
│   │   ├── routes.py           # POST /upload, GET /videos, DELETE /videos/{id}
│   │   ├── upload.py           # Lógica específica de subida con validación corregida
│   │   ├── processing.py       # Procesamiento de video (duración, thumbnails)
│   │   └── schemas.py          # VideoCreate, VideoResponse, UploadStatus
│   │
│   ├── screens/                # 📺 Gestión de Pantallas
│   │   ├── __init__.py
│   │   ├── routes.py           # CRUD completo para pantallas
│   │   ├── provisioning.py     # Lógica de aprovisionamiento de nuevas pantallas
│   │   └── schemas.py          # ScreenCreate, ScreenUpdate, ScreenStatus
│   │
│   ├── schedule/               # ⏰ Programación de Contenido
│   │   ├── __init__.py
│   │   ├── routes.py           # CRUD para reglas de programación
│   │   ├── resolver.py         # Resolución de reglas a videos activos
│   │   ├── validation.py       # Validación de horarios y conflictos
│   │   └── schemas.py          # ScheduleRule, TimeSlot, ScheduleStatus
│   │
│   ├── publish/                # 🚀 Publicación y Sincronización
│   │   ├── __init__.py
│   │   ├── routes.py           # POST /publish/screen/{id}, GET /publish/status
│   │   ├── bulk.py             # Publicación masiva con concurrencia controlada
│   │   ├── status.py           # Estado de sincronización por pantalla
│   │   └── schemas.py          # PublishRequest, SyncStatus, BulkPublishResult
│   │
│   ├── player/                 # 🎮 API Para Players (Lado Cliente)
│   │   ├── __init__.py
│   │   ├── routes.py           # GET /state, POST /heartbeat, POST /sync-confirm
│   │   ├── state.py            # Entrega de estado deseado
│   │   ├── downloads.py        # URLs de descarga firmadas
│   │   ├── health.py           # Recepción de métricas de salud
│   │   └── schemas.py          # PlayerState, DownloadInfo, HealthReport
│   │
│   ├── admin/                  # 👨‍💼 Administración de Clientes y Sistema
│   │   ├── __init__.py
│   │   ├── routes.py           # CRUD clientes, gestión de usuarios
│   │   ├── clients.py          # Lógica específica de clientes
│   │   ├── users.py            # Gestión de usuarios del sistema
│   │   ├── metrics.py          # Endpoints de métricas agregadas
│   │   └── schemas.py          # ClientCreate, UserCreate, SystemMetrics
│   │
│   └── monitoring/             # 📊 Observabilidad y Métricas
│       ├── __init__.py
│       ├── routes.py           # GET /health, GET /metrics, GET /status
│       ├── health.py           # Health checks detallados
│       ├── prometheus.py       # Métricas para Prometheus
│       └── schemas.py          # HealthStatus, MetricsData
```

#### **`src/models/` - Modelos de Datos**
```
models/
├── __init__.py
├── database.py                 # Configuración SQLAlchemy, engine, sessions
├── base.py                     # Clase base para todos los modelos
│
├── auth/                       # 🔐 Modelos de Autenticación
│   ├── __init__.py
│   ├── models.py               # User, Role, Permission (SQLAlchemy)
│   └── schemas.py              # Pydantic schemas para validación
│
├── content/                    # 📹 Modelos de Contenido
│   ├── __init__.py
│   ├── models.py               # Video, Thumbnail, VideoMetadata
│   └── schemas.py              # VideoCreate (con validación 1-20s), VideoResponse
│
├── screens/                    # 📺 Modelos de Pantallas
│   ├── __init__.py
│   ├── models.py               # Screen, ScreenCredentials, ScreenStatus
│   └── schemas.py              # ScreenCreate, ScreenUpdate, ScreenInfo
│
├── schedule/                   # ⏰ Modelos de Programación
│   ├── __init__.py
│   ├── models.py               # ScheduleRule, TimeSlot, ScheduleAssignment
│   └── schemas.py              # ScheduleCreate, ScheduleUpdate, ActiveSchedule
│
├── sync/                       # 🔄 Modelos de Sincronización
│   ├── __init__.py
│   ├── models.py               # SyncStatus, DesiredState, SyncHistory
│   └── schemas.py              # SyncRequest, SyncResponse, StateVersion
│
└── admin/                      # 👨‍💼 Modelos Administrativos
    ├── __init__.py
    ├── models.py               # Client, Subscription, AuditLog
    └── schemas.py              # ClientCreate, UserCreate, AuditEntry
```

#### **`src/services/` - Lógica de Negocio Principal**
```
services/
├── __init__.py
├── base_service.py             # Clase base con patrones comunes
│
├── auth/                       # 🔐 Servicios de Autenticación
│   ├── __init__.py
│   ├── auth_service.py         # Login, logout, refresh tokens
│   ├── jwt_service.py          # Generación y validación de JWT
│   ├── password_service.py     # Hashing y validación de contraseñas
│   └── permissions.py          # Lógica de permisos y roles
│
├── content/                    # 📹 Servicios de Contenido
│   ├── __init__.py
│   ├── content_service.py      # Upload, processing, CRUD videos
│   ├── video_processor.py      # FFmpeg, validación duración, thumbnails
│   ├── file_handler.py         # Manejo de archivos, hash, validación
│   └── metadata_extractor.py   # Extracción de metadatos de video
│
├── storage/                    # 💾 Servicios de Almacenamiento
│   ├── __init__.py
│   ├── storage_service.py      # Gestión de almacenamiento con límites
│   ├── cleanup_service.py      # Limpieza automática de assets inactivos
│   ├── minio_client.py         # Cliente MinIO para object storage
│   └── quota_manager.py        # Gestión de cuotas por cliente
│
├── scheduling/                 # ⏰ Servicios de Programación
│   ├── __init__.py
│   ├── schedule_service.py     # CRUD y lógica de programación
│   ├── rule_resolver.py        # Resolución de reglas a videos activos
│   ├── conflict_detector.py    # Detección de conflictos de horarios
│   └── time_utils.py          # Utilidades de manejo de tiempo y zonas
│
├── publishing/                 # 🚀 Servicios de Publicación
│   ├── __init__.py
│   ├── publish_service.py      # Publicación con concurrencia y locks
│   ├── state_manager.py        # Gestión de estado deseado y versionado
│   ├── sync_coordinator.py     # Coordinación de sincronización masiva
│   └── rollback_service.py     # Rollback automático en fallos
│
├── player/                     # 🎮 Servicios para Players
│   ├── __init__.py
│   ├── player_service.py       # Comunicación con players remotos
│   ├── health_monitor.py       # Monitoreo de salud de players
│   ├── download_service.py     # Generación de URLs de descarga seguras
│   └── heartbeat_service.py    # Gestión de heartbeats y estado online
│
├── monitoring/                 # 📊 Servicios de Observabilidad
│   ├── __init__.py
│   ├── metrics_service.py      # Registro y agregación de métricas
│   ├── health_service.py       # Health checks del sistema
│   ├── alert_service.py        # Generación de alertas
│   └── audit_service.py        # Registro de auditoría
│
└── notifications/              # 📢 Servicios de Notificaciones
    ├── __init__.py
    ├── notification_service.py # Envío de notificaciones
    ├── email_service.py        # Servicio de email
    ├── webhook_service.py      # Webhooks para integraciones
    └── alert_manager.py        # Gestión de alertas críticas
```

#### **`src/repositories/` - Acceso a Datos**
```
repositories/
├── __init__.py
├── base_repository.py          # Clase base con operaciones CRUD comunes
├── unit_of_work.py            # Patrón Unit of Work para transacciones
│
├── content_repository.py       # Acceso a datos de videos y contenido
├── screen_repository.py        # Acceso a datos de pantallas
├── schedule_repository.py      # Acceso a datos de programación
├── user_repository.py          # Acceso a datos de usuarios
├── client_repository.py        # Acceso a datos de clientes
├── sync_repository.py          # Acceso a datos de sincronización
├── audit_repository.py         # Acceso a logs de auditoría
└── metrics_repository.py       # Acceso a datos de métricas históricas
```

#### **`src/config/` - Configuración del Sistema**
```
config/
├── __init__.py
├── settings.py                 # Configuración principal con Pydantic Settings
├── database.py                 # Configuración específica de base de datos
├── storage.py                  # Configuración de MinIO/S3
├── redis.py                    # Configuración de Redis
├── jwt.py                      # Configuración de JWT
├── logging.py                  # Configuración detallada de logging
└── environments/               # Configuraciones por ambiente
    ├── development.py
    ├── staging.py
    ├── production.py
    └── testing.py
```

#### **`src/middleware/` - Middleware Personalizado**
```
middleware/
├── __init__.py
├── auth_middleware.py          # Middleware de autenticación JWT
├── cors_middleware.py          # Configuración CORS avanzada
├── rate_limit_middleware.py    # Rate limiting por cliente/endpoint
├── request_id_middleware.py    # Tracking de requests con IDs únicos
├── metrics_middleware.py       # Recolección automática de métricas
├── error_handler.py           # Manejo centralizado de errores
└── security_headers.py        # Headers de seguridad HTTP
```

#### **`src/utils/` - Utilidades y Helpers**
```
utils/
├── __init__.py
├── security/                   # 🔒 Utilidades de Seguridad
│   ├── __init__.py
│   ├── crypto.py               # Encriptación, hashing, firmas
│   ├── jwt_utils.py            # Utilidades específicas de JWT
│   ├── api_keys.py             # Generación y validación de API keys
│   └── rate_limiting.py        # Implementación de rate limiting
│
├── video/                      # 📹 Utilidades de Video
│   ├── __init__.py
│   ├── ffmpeg_wrapper.py       # Wrapper para operaciones FFmpeg
│   ├── thumbnail_generator.py  # Generación de thumbnails
│   ├── duration_validator.py   # Validación de duración (1-20s)
│   ├── format_converter.py     # Conversión de formatos
│   └── metadata_extractor.py   # Extracción de metadatos
│
├── file/                       # 📁 Utilidades de Archivos
│   ├── __init__.py
│   ├── hash_calculator.py      # Cálculo de hashes SHA256
│   ├── file_validator.py       # Validación de tipos de archivo
│   ├── size_calculator.py      # Cálculo de tamaños
│   └── mime_detector.py        # Detección de tipos MIME
│
├── network/                    # 🌐 Utilidades de Red
│   ├── __init__.py
│   ├── http_client.py          # Cliente HTTP con retry y timeout
│   ├── url_signer.py           # Generación de URLs firmadas
│   ├── ip_utils.py             # Utilidades de direcciones IP
│   └── tailscale_client.py     # Cliente para Tailscale API
│
├── time/                       # ⏰ Utilidades de Tiempo
│   ├── __init__.py
│   ├── timezone_handler.py     # Manejo de zonas horarias
│   ├── schedule_calculator.py  # Cálculos de horarios
│   └── duration_formatter.py   # Formateo de duraciones
│
└── validation/                 # ✅ Utilidades de Validación
    ├── __init__.py
    ├── schema_validator.py     # Validación de esquemas JSON
    ├── business_rules.py       # Reglas de negocio
    ├── sanitization.py         # Sanitización de datos
    └── constraints.py          # Validaciones de constraints
```

---

## 🖥️ Frontend (`/frontend`) - Interfaz Web de Administración

### **Estructura General**
```
frontend/
├── package.json                # Dependencias y scripts de Node.js
├── package-lock.json          # Lock file para dependencias
├── next.config.js             # Configuración Next.js 14
├── tailwind.config.js         # Configuración Tailwind CSS
├── tsconfig.json              # Configuración TypeScript
├── eslint.config.js           # Configuración ESLint
├── prettier.config.js         # Configuración Prettier
├── Dockerfile                 # Imagen Docker para producción
└── .env.local.example         # Plantilla de variables de entorno
```

### **`src/app/` - App Router (Next.js 14)**
```
app/
├── layout.tsx                 # Layout principal con providers
├── page.tsx                   # Página de inicio/landing
├── globals.css                # Estilos globales con Tailwind
├── loading.tsx                # Componente de loading global
├── error.tsx                  # Página de error global
├── not-found.tsx              # Página 404 personalizada
│
├── (auth)/                    # 🔐 Grupo de rutas de autenticación
│   ├── layout.tsx             # Layout específico para auth
│   ├── login/
│   │   ├── page.tsx           # Página de login
│   │   └── loading.tsx
│   ├── register/
│   │   └── page.tsx           # Registro de nuevos usuarios
│   └── forgot-password/
│       └── page.tsx           # Recuperación de contraseña
│
├── (dashboard)/               # 🏠 Grupo de rutas del dashboard
│   ├── layout.tsx             # Layout con sidebar y navegación
│   ├── loading.tsx            # Loading para toda la sección
│   │
│   ├── dashboard/             # Dashboard principal
│   │   ├── page.tsx           # Overview con métricas principales
│   │   ├── loading.tsx
│   │   └── components/
│   │       ├── metrics-cards.tsx
│   │       ├── recent-activity.tsx
│   │       └── quick-actions.tsx
│   │
│   ├── content/               # 📹 Gestión de Contenido
│   │   ├── page.tsx           # Lista de videos
│   │   ├── loading.tsx
│   │   ├── upload/
│   │   │   ├── page.tsx       # Página de subida (validación 1-20s)
│   │   │   └── components/
│   │   │       ├── video-uploader.tsx
│   │   │       ├── upload-progress.tsx
│   │   │       └── validation-feedback.tsx
│   │   ├── [id]/
│   │   │   ├── page.tsx       # Detalle de video individual
│   │   │   ├── edit/
│   │   │   │   └── page.tsx   # Edición de metadatos
│   │   │   └── components/
│   │   │       ├── video-preview.tsx
│   │   │       └── metadata-form.tsx
│   │   └── components/
│   │       ├── content-grid.tsx
│   │       ├── content-filters.tsx
│   │       ├── bulk-actions.tsx
│   │       └── video-card.tsx
│   │
│   ├── screens/               # 📺 Gestión de Pantallas
│   │   ├── page.tsx           # Lista de pantallas
│   │   ├── loading.tsx
│   │   ├── new/
│   │   │   └── page.tsx       # Crear nueva pantalla
│   │   ├── [id]/
│   │   │   ├── page.tsx       # Detalle de pantalla
│   │   │   ├── edit/
│   │   │   │   └── page.tsx   # Editar configuración
│   │   │   ├── schedule/
│   │   │   │   └── page.tsx   # Programación específica
│   │   │   └── logs/
│   │   │       └── page.tsx   # Logs de sincronización
│   │   └── components/
│   │       ├── screen-grid.tsx
│   │       ├── screen-status-badge.tsx
│   │       ├── screen-form.tsx
│   │       ├── sync-status.tsx
│   │       └── screen-metrics.tsx
│   │
│   ├── schedule/              # ⏰ Programación de Contenido
│   │   ├── page.tsx           # Vista general de programación
│   │   ├── calendar/
│   │   │   └── page.tsx       # Vista de calendario
│   │   ├── rules/
│   │   │   ├── page.tsx       # Gestión de reglas
│   │   │   └── new/
│   │   │       └── page.tsx   # Crear nueva regla
│   │   └── components/
│   │       ├── schedule-calendar.tsx
│   │       ├── time-slot-editor.tsx
│   │       ├── rule-builder.tsx
│   │       ├── conflict-detector.tsx
│   │       └── schedule-preview.tsx
│   │
│   ├── analytics/             # 📊 Analytics y Reportes
│   │   ├── page.tsx           # Dashboard de analytics
│   │   ├── reports/
│   │   │   └── page.tsx       # Reportes detallados
│   │   ├── performance/
│   │   │   └── page.tsx       # Métricas de rendimiento
│   │   └── components/
│   │       ├── analytics-charts.tsx
│   │       ├── performance-metrics.tsx
│   │       ├── report-generator.tsx
│   │       └── data-export.tsx
│   │
│   └── settings/              # ⚙️ Configuración del Sistema
│       ├── page.tsx           # Configuración general
│       ├── users/
│       │   ├── page.tsx       # Gestión de usuarios
│       │   └── [id]/
│       │       └── page.tsx   # Detalle de usuario
│       ├── clients/
│       │   ├── page.tsx       # Gestión de clientes
│       │   └── [id]/
│       │       └── page.tsx   # Configuración de cliente
│       ├── system/
│       │   └── page.tsx       # Configuración del sistema
│       └── components/
│           ├── user-management.tsx
│           ├── client-settings.tsx
│           ├── system-config.tsx
│           └── permissions-matrix.tsx
│
└── api/                       # 🔌 API Routes (si es necesario)
    ├── auth/
    │   └── route.ts           # Proxy para autenticación
    ├── upload/
    │   └── route.ts           # Upload directo al frontend
    └── webhooks/
        └── route.ts           # Webhooks de terceros
```

### **`src/components/` - Componentes React Reutilizables**
```
components/
├── ui/                        # 🎨 Componentes Básicos de UI
│   ├── button.tsx             # Botón con variantes
│   ├── input.tsx              # Input con validación
│   ├── textarea.tsx           # Textarea con auto-resize
│   ├── select.tsx             # Select con búsqueda
│   ├── checkbox.tsx           # Checkbox personalizado
│   ├── radio.tsx              # Radio buttons
│   ├── switch.tsx             # Toggle switch
│   ├── slider.tsx             # Slider para rangos
│   ├── progress.tsx           # Barra de progreso
│   ├── spinner.tsx            # Indicador de carga
│   ├── badge.tsx              # Badges de estado
│   ├── avatar.tsx             # Avatar de usuario
│   ├── tooltip.tsx            # Tooltips informativos
│   ├── popover.tsx            # Popovers
│   ├── modal.tsx              # Modal/Dialog
│   ├── alert.tsx              # Alertas y notificaciones
│   ├── card.tsx               # Cards contenedores
│   ├── table.tsx              # Tabla con sorting/filtering
│   ├── pagination.tsx         # Paginación
│   ├── tabs.tsx               # Tabs navigation
│   ├── accordion.tsx          # Accordion/Collapsible
│   ├── breadcrumb.tsx         # Breadcrumb navigation
│   └── skeleton.tsx           # Skeleton loading
│
├── forms/                     # 📝 Componentes de Formularios
│   ├── video-uploader.tsx     # Uploader con validación 1-20s ✅
│   ├── drag-drop-zone.tsx     # Zona de drag & drop
│   ├── file-preview.tsx       # Preview de archivos
│   ├── form-field.tsx         # Wrapper de campos de formulario
│   ├── form-section.tsx       # Secciones de formulario
│   ├── validation-message.tsx # Mensajes de validación
│   ├── screen-form.tsx        # Formulario de pantallas
│   ├── schedule-form.tsx      # Formulario de programación
│   ├── user-form.tsx          # Formulario de usuarios
│   ├── client-form.tsx        # Formulario de clientes
│   └── bulk-actions.tsx       # Acciones masivas
│
├── layout/                    # 🏗️ Componentes de Layout
│   ├── header.tsx             # Header principal con navegación
│   ├── sidebar.tsx            # Sidebar con menú
│   ├── navigation.tsx         # Navegación principal
│   ├── breadcrumbs.tsx        # Breadcrumbs automáticos
│   ├── page-header.tsx        # Header de página con acciones
│   ├── content-wrapper.tsx    # Wrapper de contenido
│   ├── footer.tsx             # Footer
│   └── mobile-nav.tsx         # Navegación móvil
│
├── data-display/              # 📊 Componentes de Visualización
│   ├── data-table.tsx         # Tabla avanzada con sorting/filtering
│   ├── grid-view.tsx          # Vista de grilla
│   ├── list-view.tsx          # Vista de lista
│   ├── metrics-card.tsx       # Tarjetas de métricas
│   ├── status-indicator.tsx   # Indicadores de estado
│   ├── progress-bar.tsx       # Barras de progreso detalladas
│   ├── chart-wrapper.tsx      # Wrapper para gráficos
│   ├── empty-state.tsx        # Estados vacíos
│   ├── error-boundary.tsx     # Boundary de errores
│   └── loading-state.tsx      # Estados de carga
│
├── media/                     # 🎬 Componentes de Media
│   ├── video-player.tsx       # Reproductor de video
│   ├── video-thumbnail.tsx    # Thumbnails de video
│   ├── video-preview.tsx      # Preview modal de video
│   ├── image-viewer.tsx       # Visor de imágenes
│   ├── media-gallery.tsx      # Galería de media
│   └── duration-display.tsx   # Display de duración
│
├── scheduling/                # ⏰ Componentes de Programación
│   ├── calendar-view.tsx      # Vista de calendario
│   ├── time-picker.tsx        # Selector de tiempo
│   ├── date-range-picker.tsx  # Selector de rango de fechas
│   ├── schedule-timeline.tsx  # Timeline de programación
│   ├── rule-builder.tsx       # Constructor de reglas
│   ├── conflict-detector.tsx  # Detector de conflictos
│   └── schedule-preview.tsx   # Preview de programación
│
├── monitoring/                # 📈 Componentes de Monitoreo
│   ├── health-indicator.tsx   # Indicador de salud
│   ├── sync-status.tsx        # Estado de sincronización
│   ├── player-status.tsx      # Estado de players
│   ├── metrics-chart.tsx      # Gráficos de métricas
│   ├── alert-panel.tsx        # Panel de alertas
│   ├── log-viewer.tsx         # Visor de logs
│   └── performance-monitor.tsx # Monitor de rendimiento
│
└── common/                    # 🔧 Componentes Comunes
    ├── search-box.tsx         # Caja de búsqueda
    ├── filter-panel.tsx       # Panel de filtros
    ├── sort-controls.tsx      # Controles de ordenamiento
    ├── export-button.tsx      # Botón de exportación
    ├── refresh-button.tsx     # Botón de refresh
    ├── action-menu.tsx        # Menú de acciones
    ├── confirmation-dialog.tsx # Diálogo de confirmación
    ├── copy-to-clipboard.tsx  # Copiar al portapapeles
    ├── keyboard-shortcuts.tsx # Atajos de teclado
    └── theme-toggle.tsx       # Toggle de tema
```

### **`src/lib/` - Librerías y Utilidades**
```
lib/
├── api/                       # 🌐 Cliente API
│   ├── client.ts              # Cliente HTTP base con interceptors
│   ├── auth.ts                # Endpoints de autenticación
│   ├── content.ts             # Endpoints de contenido
│   ├── screens.ts             # Endpoints de pantallas
│   ├── schedule.ts            # Endpoints de programación
│   ├── admin.ts               # Endpoints de administración
│   ├── monitoring.ts          # Endpoints de monitoreo
│   └── types.ts               # Tipos TypeScript para API
│
├── auth/                      # 🔐 Autenticación
│   ├── auth-provider.tsx      # Provider de contexto de auth
│   ├── use-auth.ts            # Hook de autenticación
│   ├── token-manager.ts       # Gestión de tokens
│   ├── permissions.ts         # Lógica de permisos
│   └── auth-guard.tsx         # Guard para rutas protegidas
│
├── validation/                # ✅ Validación
│   ├── schemas.ts             # Esquemas Zod para formularios
│   ├── video-validation.ts    # Validación específica de videos
│   ├── form-validation.ts     # Validaciones de formularios
│   └── custom-validators.ts   # Validadores personalizados
│
├── utils/                     # 🛠️ Utilidades
│   ├── cn.ts                  # Utility para clases CSS (classnames)
│   ├── format.ts              # Formateo de datos (tamaños, duraciones)
│   ├── date.ts                # Utilidades de fechas y tiempo
│   ├── file.ts                # Utilidades de archivos
│   ├── string.ts              # Utilidades de strings
│   ├── number.ts              # Utilidades numéricas
│   ├── url.ts                 # Utilidades de URLs
│   ├── debounce.ts            # Debounce y throttle
│   ├── local-storage.ts       # Gestión de localStorage
│   ├── constants.ts           # Constantes del frontend
│   └── errors.ts              # Manejo de errores
│
├── hooks/                     # 🎣 Custom React Hooks
│   ├── use-api.ts             # Hook para llamadas API
│   ├── use-auth.ts            # Hook de autenticación
│   ├── use-video-validation.ts # Hook para validación de videos
│   ├── use-local-storage.ts   # Hook para localStorage
│   ├── use-debounce.ts        # Hook de debounce
│   ├── use-intersection.ts    # Hook de intersection observer
│   ├── use-media-query.ts     # Hook para media queries
│   ├── use-clipboard.ts       # Hook para portapapeles
│   ├── use-websocket.ts       # Hook para WebSockets
│   ├── use-upload.ts          # Hook para subida de archivos
│   ├── use-pagination.ts      # Hook para paginación
│   ├── use-sorting.ts         # Hook para ordenamiento
│   ├── use-filtering.ts       # Hook para filtrado
│   └── use-real-time.ts       # Hook para actualizaciones en tiempo real
│
├── stores/                    # 🏪 Estado Global (Zustand)
│   ├── auth-store.ts          # Store de autenticación
│   ├── content-store.ts       # Store de contenido
│   ├── screens-store.ts       # Store de pantallas
│   ├── schedule-store.ts      # Store de programación
│   ├── ui-store.ts            # Store de UI (modals, sidebars)
│   ├── upload-store.ts        # Store de uploads
│   ├── notifications-store.ts # Store de notificaciones
│   └── settings-store.ts      # Store de configuraciones
│
├── providers/                 # 🔌 React Providers
│   ├── query-provider.tsx     # TanStack Query provider
│   ├── theme-provider.tsx     # Provider de tema
│   ├── toast-provider.tsx     # Provider de notificaciones
│   ├── modal-provider.tsx     # Provider de modales
│   └── app-providers.tsx      # Combinación de todos los providers
│
└── types/                     # 📝 Tipos TypeScript
    ├── api.ts                 # Tipos de API responses
    ├── auth.ts                # Tipos de autenticación
    ├── content.ts             # Tipos de contenido
    ├── screens.ts             # Tipos de pantallas
    ├── schedule.ts            # Tipos de programación
    ├── ui.ts                  # Tipos de UI
    ├── forms.ts               # Tipos de formularios
    ├── common.ts              # Tipos comunes
    └── global.d.ts            # Tipos globales
```

---

## 📺 Player (`/player`) - Software del Dispositivo de Reproducción

### **Estructura General**
```
player/
├── requirements.txt           # Dependencias Python principales
├── requirements-dev.txt       # Dependencias de desarrollo
├── config.yaml               # Configuración principal del player
├── Dockerfile                # Imagen Docker para player
├── docker-compose.yml        # Compose para testing local
├── pyproject.toml            # Configuración moderna de Python
├── setup.py                  # Setup script para instalación
└── README.md                 # Documentación específica del player
```

### **`src/` - Código Fuente del Player**

#### **`src/core/` - Componentes Principales**
```
core/
├── __init__.py
├── main.py                   # Aplicación principal del player
├── app.py                    # Configuración de la aplicación Flask/FastAPI
│
├── reconciler.py             # 🔄 Reconciliación Robusta con Manejo de Errores
│   # - Lógica de sincronización con backoff exponencial
│   # - Manejo de fallos de red con retry automático
│   # - Rollback automático en fallos de aplicación
│   # - Versionado optimista para evitar race conditions
│
├── network/                  # 🌐 Gestión de Red
│   ├── __init__.py
│   ├── manager.py            # NetworkManager con retry y timeout
│   ├── http_client.py        # Cliente HTTP robusto
│   ├── connection_monitor.py # Monitor de conectividad
│   ├── tailscale_client.py   # Cliente específico para Tailscale
│   └── offline_mode.py       # Modo offline cuando no hay conexión
│
├── storage/                  # 💾 Gestión de Almacenamiento Local
│   ├── __init__.py
│   ├── manager.py            # StorageManager con limpieza automática
│   ├── asset_cache.py        # Cache de assets con LRU
│   ├── integrity_checker.py  # Verificación de integridad de archivos
│   ├── cleanup_service.py    # Limpieza automática de assets inactivos
│   ├── quota_manager.py      # Gestión de cuotas de almacenamiento
│   └── file_organizer.py     # Organización de archivos por fecha/tipo
│
├── playlist/                 # 🎵 Gestión de Playlists
│   ├── __init__.py
│   ├── manager.py            # PlaylistManager con aplicación atómica
│   ├── player_engine.py      # Motor de reproducción de video
│   ├── scheduler.py          # Programador de reproducción
│   ├── transition_manager.py # Gestión de transiciones entre videos
│   └── loop_controller.py    # Control de loops y repeticiones
│
├── monitoring/               # 📊 Monitoreo y Métricas
│   ├── __init__.py
│   ├── service.py            # MonitoringService con reporte al servidor
│   ├── health_checker.py     # Health checks del sistema
│   ├── metrics_collector.py  # Recolector de métricas del sistema
│   ├── performance_monitor.py # Monitor de rendimiento
│   ├── sync_metrics.py       # Métricas específicas de sincronización
│   └── alert_manager.py      # Gestión de alertas locales
│
├── sync/                     # 🔄 Sincronización con Servidor
│   ├── __init__.py
│   ├── coordinator.py        # Coordinador principal de sincronización
│   ├── state_manager.py      # Gestión de estado local vs remoto
│   ├── version_tracker.py    # Tracking de versiones aplicadas
│   ├── conflict_resolver.py  # Resolución de conflictos de estado
│   └── heartbeat_service.py  # Servicio de heartbeat al servidor
│
├── hardware/                 # ⚙️ Interfaz con Hardware
│   ├── __init__.py
│   ├── display_manager.py    # Gestión de pantallas y resoluciones
│   ├── gpu_monitor.py        # Monitor de GPU para reproducción
│   ├── thermal_monitor.py    # Monitor de temperatura
│   ├── power_manager.py      # Gestión de energía
│   └── peripheral_detector.py # Detección de periféricos
│
└── security/                 # 🔒 Seguridad del Player
    ├── __init__.py
    ├── api_key_manager.py    # Gestión de claves API
    ├── certificate_manager.py # Gestión de certificados TLS
    ├── secure_storage.py     # Almacenamiento seguro de credenciales
    ├── access_control.py     # Control de acceso a APIs locales
    └── audit_logger.py       # Logging de auditoría de seguridad
```

#### **`src/models/` - Modelos de Datos del Player**
```
models/
├── __init__.py
├── config/                   # 📋 Configuración
│   ├── __init__.py
│   ├── player_config.py      # Configuración principal del player
│   ├── network_config.py     # Configuración de red
│   ├── storage_config.py     # Configuración de almacenamiento
│   ├── display_config.py     # Configuración de pantalla
│   └── security_config.py    # Configuración de seguridad
│
├── sync/                     # 🔄 Sincronización
│   ├── __init__.py
│   ├── sync_state.py         # Estado de sincronización
│   ├── desired_state.py      # Estado deseado del servidor
│   ├── applied_state.py      # Estado aplicado localmente
│   ├── sync_history.py       # Historial de sincronizaciones
│   └── version_info.py       # Información de versiones
│
├── content/                  # 📹 Contenido
│   ├── __init__.py
│   ├── video_asset.py        # Modelo de asset de video
│   ├── playlist.py           # Modelo de playlist
│   ├── content_metadata.py   # Metadatos de contenido
│   └── download_info.py      # Información de descarga
│
├── system/                   # 💻 Sistema
│   ├── __init__.py
│   ├── system_info.py        # Información del sistema
│   ├── hardware_status.py    # Estado del hardware
│   ├── performance_metrics.py # Métricas de rendimiento
│   └── health_status.py      # Estado de salud general
│
└── api/                      # 🔌 API
    ├── __init__.py
    ├── request_models.py     # Modelos de request
    ├── response_models.py    # Modelos de response
    └── error_models.py       # Modelos de error
```

#### **`src/api/` - API Local del Player**
```
api/
├── __init__.py
├── app.py                    # Aplicación Flask/FastAPI local
├── middleware.py             # Middleware de autenticación local
│
├── endpoints/                # 🔗 Endpoints de la API Local
│   ├── __init__.py
│   ├── status.py             # GET /status - Estado general
│   ├── health.py             # GET /health - Health check detallado
│   ├── sync.py               # POST /sync - Forzar sincronización
│   ├── assets.py             # GET /assets - Estado de assets
│   ├── playlist.py           # GET /playlist - Playlist actual
│   ├── metrics.py            # GET /metrics - Métricas en formato Prometheus
│   ├── logs.py               # GET /logs - Logs del sistema
│   ├── config.py             # GET/PUT /config - Configuración
│   ├── system.py             # GET /system - Información del sistema
│   └── emergency.py          # POST /emergency - Comandos de emergencia
│
└── auth/                     # 🔐 Autenticación Local
    ├── __init__.py
    ├── api_key_auth.py       # Autenticación por API key
    ├── local_auth.py         # Autenticación local
    └── middleware.py         # Middleware de auth
```

#### **`src/utils/` - Utilidades del Player**
```
utils/
├── __init__.py
├── system/                   # 💻 Utilidades de Sistema
│   ├── __init__.py
│   ├── process_manager.py    # Gestión de procesos
│   ├── service_manager.py    # Gestión de servicios systemd
│   ├── log_rotator.py        # Rotación de logs
│   ├── backup_manager.py     # Backup de configuración
│   └── update_manager.py     # Gestión de actualizaciones
│
├── video/                    # 🎬 Utilidades de Video
│   ├── __init__.py
│   ├── player_wrapper.py     # Wrapper para reproductores (VLC, MPV)
│   ├── codec_detector.py     # Detección de codecs
│   ├── resolution_manager.py # Gestión de resoluciones
│   ├── subtitle_manager.py   # Gestión de subtítulos
│   └── audio_manager.py      # Gestión de audio
│
├── network/                  # 🌐 Utilidades de Red
│   ├── __init__.py
│   ├── bandwidth_monitor.py  # Monitor de ancho de banda
│   ├── connectivity_test.py  # Tests de conectividad
│   ├── dns_resolver.py       # Resolución DNS
│   ├── proxy_detector.py     # Detección de proxies
│   └── latency_monitor.py    # Monitor de latencia
│
├── file/                     # 📁 Utilidades de Archivos
│   ├── __init__.py
│   ├── file_watcher.py       # Watcher de archivos
│   ├── disk_monitor.py       # Monitor de disco
│   ├── compression.py        # Compresión/descompresión
│   ├── checksum_validator.py # Validación de checksums
│   └── mime_detector.py      # Detección de tipos MIME
│
├── security/                 # 🔒 Utilidades de Seguridad
│   ├── __init__.py
│   ├── crypto_utils.py       # Utilidades criptográficas
│   ├── key_derivation.py     # Derivación de claves
│   ├── secure_delete.py      # Eliminación segura de archivos
│   └── permission_checker.py # Verificación de permisos
│
└── logging/                  # 📝 Utilidades de Logging
    ├── __init__.py
    ├── structured_logger.py  # Logger estructurado
    ├── remote_logger.py      # Envío de logs al servidor
    ├── log_formatter.py      # Formateo de logs
    ├── log_filter.py         # Filtros de logs
    └── performance_logger.py # Logging de performance
```

### **`config/` - Configuraciones por Ambiente**
```
config/
├── default.yaml              # Configuración por defecto
├── development.yaml          # Configuración para desarrollo
├── staging.yaml              # Configuración para staging
├── production.yaml           # Configuración para producción
├── testing.yaml              # Configuración para tests
│
├── templates/                # Plantillas de configuración
│   ├── basic-player.yaml     # Player básico
│   ├── high-performance.yaml # Player de alto rendimiento
│   ├── low-bandwidth.yaml    # Player para bajo ancho de banda
│   └── kiosk-mode.yaml       # Modo kiosko
│
└── schemas/                  # Esquemas de validación
    ├── config-schema.json    # Schema JSON para validación
    └── environment-vars.md   # Documentación de variables
```

### **`scripts/` - Scripts de Instalación y Mantenimiento**
```
scripts/
├── installation/             # 📦 Scripts de Instalación
│   ├── install.sh            # Script principal de instalación
│   ├── setup-environment.sh  # Configuración del entorno
│   ├── install-dependencies.sh # Instalación de dependencias
│   ├── configure-systemd.sh  # Configuración de servicios systemd
│   ├── setup-autostart.sh    # Configuración de autostart
│   └── security-hardening.sh # Hardening de seguridad
│
├── maintenance/              # 🔧 Scripts de Mantenimiento
│   ├── cleanup_storage.py    # Limpieza de almacenamiento
│   ├── health_check.py       # Verificación de salud
│   ├── log_cleanup.py        # Limpieza de logs
│   ├── backup_config.py      # Backup de configuración
│   ├── restore_config.py     # Restauración de configuración
│   ├── update_player.py      # Actualización del player
│   └── reset_player.py       # Reset completo del player
│
├── monitoring/               # 📊 Scripts de Monitoreo
│   ├── system_monitor.py     # Monitor del sistema
│   ├── network_test.py       # Test de conectividad
│   ├── performance_test.py   # Test de rendimiento
│   ├── stress_test.py        # Test de estrés
│   └── benchmark.py          # Benchmark del sistema
│
├── development/              # 🛠️ Scripts de Desarrollo
│   ├── dev_setup.py          # Setup para desarrollo
│   ├── mock_server.py        # Servidor mock para testing
│   ├── simulate_scenarios.py # Simulación de escenarios
│   └── generate_test_data.py # Generación de datos de prueba
│
└── deployment/               # 🚀 Scripts de Despliegue
    ├── deploy_to_device.py   # Despliegue a dispositivo
    ├── bulk_deploy.py        # Despliegue masivo
    ├── rollback.py           # Rollback de versión
    └── validate_deployment.py # Validación post-despliegue
```

### **`systemd/` - Servicios del Sistema**
```
systemd/
├── avtech-player.service     # Servicio principal del player
├── avtech-updater.service    # Servicio de actualización automática
├── avtech-monitor.service    # Servicio de monitoreo
├── avtech-cleanup.service    # Servicio de limpieza programada
├── avtech-backup.service     # Servicio de backup
│
├── timers/                   # Timers de systemd
│   ├── avtech-cleanup.timer  # Timer para limpieza
│   ├── avtech-backup.timer   # Timer para backup
│   ├── avtech-healthcheck.timer # Timer para health checks
│   └── avtech-sync.timer     # Timer para sincronización forzada
│
└── overrides/                # Overrides específicos
    ├── raspberry-pi.conf     # Configuración para Raspberry Pi
    ├── intel-nuc.conf        # Configuración para Intel NUC
    └── vm-config.conf        # Configuración para VMs
```

---

## 🔗 Shared (`/shared`) - Código Compartido

### **Estructura del Directorio Shared**
```
shared/
├── __init__.py
├── pyproject.toml            # Configuración del paquete compartido
├── setup.py                  # Setup para instalación como paquete
│
├── models/                   # 📋 Modelos Compartidos
│   ├── __init__.py
│   ├── sync_protocol.py      # Protocolo de sincronización backend-player
│   ├── content_models.py     # Modelos de contenido comunes
│   ├── api_responses.py      # Modelos de respuesta API estandarizados
│   ├── error_models.py       # Modelos de error consistentes
│   ├── metrics_models.py     # Modelos de métricas
│   ├── health_models.py      # Modelos de health checks
│   └── configuration_models.py # Modelos de configuración
│
├── protocols/                # 🔄 Protocolos de Comunicación
│   ├── __init__.py
│   ├── sync_v1.py            # Protocolo de sincronización v1
│   ├── heartbeat.py          # Protocolo de heartbeat
│   ├── download.py           # Protocolo de descarga de assets
│   ├── metrics.py            # Protocolo de envío de métricas
│   └── emergency.py          # Protocolo de comandos de emergencia
│
├── utils/                    # 🛠️ Utilidades Compartidas
│   ├── __init__.py
│   ├── constants.py          # Constantes del sistema
│   ├── validation.py         # Validaciones comunes
│   ├── crypto.py             # Utilidades criptográficas compartidas
│   ├── serialization.py      # Serialización/deserialización
│   ├── time_utils.py         # Utilidades de tiempo consistentes
│   ├── file_utils.py         # Utilidades de archivos
│   ├── network_utils.py      # Utilidades de red
│   └── logging_utils.py      # Configuración de logging consistente
│
├── exceptions/               # ❌ Excepciones Comunes
│   ├── __init__.py
│   ├── base_exceptions.py    # Excepciones base
│   ├── sync_exceptions.py    # Excepciones de sincronización
│   ├── content_exceptions.py # Excepciones de contenido
│   ├── network_exceptions.py # Excepciones de red
│   └── validation_exceptions.py # Excepciones de validación
│
├── schemas/                  # 📝 Esquemas de Validación
│   ├── __init__.py
│   ├── json_schemas/         # Esquemas JSON Schema
│   │   ├── sync_request.json
│   │   ├── player_state.json
│   │   ├── content_metadata.json
│   │   └── health_report.json
│   ├── pydantic_schemas.py   # Esquemas Pydantic
│   └── validation_rules.py   # Reglas de validación comunes
│
└── testing/                  # 🧪 Utilidades de Testing
    ├── __init__.py
    ├── fixtures.py           # Fixtures comunes para tests
    ├── mocks.py              # Mocks compartidos
    ├── factories.py          # Factories para crear datos de prueba
    ├── assertions.py         # Assertions personalizadas
    └── test_helpers.py       # Helpers para tests
```

---

## 🏗️ Infra (`/infra`) - Infraestructura como Código

### **Estructura de Infraestructura**
```
infra/
├── README.md                 # Documentación de infraestructura
├── .gitignore               # Ignorar archivos sensibles
│
├── docker/                  # 🐳 Configuraciones Docker
│   ├── backend/
│   │   ├── Dockerfile        # Dockerfile optimizado para backend
│   │   ├── Dockerfile.dev    # Dockerfile para desarrollo
│   │   └── entrypoint.sh     # Script de entrada
│   ├── frontend/
│   │   ├── Dockerfile        # Dockerfile para frontend
│   │   ├── Dockerfile.dev    # Dockerfile para desarrollo
│   │   └── nginx.conf        # Configuración Nginx
│   ├── player/
│   │   ├── Dockerfile        # Dockerfile para player
│   │   ├── Dockerfile.arm64  # Para arquitecturas ARM
│   │   └── init.sh           # Script de inicialización
│   ├── monitoring/
│   │   ├── prometheus/
│   │   │   ├── Dockerfile
│   │   │   └── prometheus.yml
│   │   ├── grafana/
│   │   │   ├── Dockerfile
│   │   │   └── dashboards/
│   │   └── alertmanager/
│   │       ├── Dockerfile
│   │       └── alertmanager.yml
│   ├── databases/
│   │   ├── postgres/
│   │   │   ├── Dockerfile
│   │   │   ├── init.sql
│   │   │   └── pg_hba.conf
│   │   └── redis/
│   │       ├── Dockerfile
│   │       └── redis.conf
│   │
│   ├── compose/              # Docker Compose files
│   │   ├── docker-compose.yml # Producción
│   │   ├── docker-compose.dev.yml # Desarrollo
│   │   ├── docker-compose.staging.yml # Staging
│   │   ├── docker-compose.monitoring.yml # Monitoreo
│   │   └── docker-compose.override.yml.example
│   │
│   └── registry/             # Configuración de registry privado
│       ├── config.yml
│       └── auth/
│
├── terraform/               # 🌍 Infraestructura en la Nube
│   ├── main.tf              # Configuración principal
│   ├── variables.tf         # Variables de entrada
│   ├── outputs.tf           # Outputs
│   ├── providers.tf         # Configuración de providers
│   ├── versions.tf          # Versiones de Terraform
│   │
│   ├── environments/        # Configuraciones por ambiente
│   │   ├── development/
│   │   │   ├── main.tf
│   │   │   ├── terraform.tfvars
│   │   │   └── backend.tf
│   │   ├── staging/
│   │   │   ├── main.tf
│   │   │   ├── terraform.tfvars
│   │   │   └── backend.tf
│   │   └── production/
│   │       ├── main.tf
│   │       ├── terraform.tfvars
│   │       └── backend.tf
│   │
│   └── modules/             # Módulos reutilizables
│       ├── vpc/
│       │   ├── main.tf
│       │   ├── variables.tf
│       │   ├── outputs.tf
│       │   └── README.md
│       ├── database/
│       │   ├── main.tf
│       │   ├── variables.tf
│       │   ├── outputs.tf
│       │   └── README.md
│       ├── compute/
│       │   ├── main.tf
│       │   ├── variables.tf
│       │   ├── outputs.tf
│       │   └── README.md
│       ├── storage/
│       │   ├── main.tf
│       │   ├── variables.tf
│       │   ├── outputs.tf
│       │   └── README.md
│       ├── monitoring/
│       │   ├── main.tf
│       │   ├── variables.tf
│       │   ├── outputs.tf
│       │   └── README.md
│       └── security/
│           ├── main.tf
│           ├── variables.tf
│           ├── outputs.tf
│           └── README.md
│
├── ansible/                 # 📦 Configuración de Servidores
│   ├── ansible.cfg          # Configuración de Ansible
│   ├── requirements.yml     # Roles y collections requeridas
│   │
│   ├── inventory/           # Inventarios
│   │   ├── development/
│   │   │   ├── hosts.yml
│   │   │   └── group_vars/
│   │   ├── staging/
│   │   │   ├── hosts.yml
│   │   │   └── group_vars/
│   │   ├── production/
│   │   │   ├── hosts.yml
│   │   │   └── group_vars/
│   │   └── dynamic/
│   │       └── aws_ec2.yml
│   │
│   ├── playbooks/           # Playbooks principales
│   │   ├── site.yml         # Playbook principal
│   │   ├── setup-server.yml # Configuración inicial del servidor
│   │   ├── deploy-backend.yml # Despliegue del backend
│   │   ├── deploy-frontend.yml # Despliegue del frontend
│   │   ├── install-player.yml # Instalación del player
│   │   ├── update-system.yml # Actualizaciones del sistema
│   │   ├── backup.yml       # Backup de sistemas
│   │   ├── monitoring.yml   # Configuración de monitoreo
│   │   └── security.yml     # Hardening de seguridad
│   │
│   ├── roles/               # Roles personalizados
│   │   ├── common/
│   │   │   ├── tasks/
│   │   │   ├── handlers/
│   │   │   ├── templates/
│   │   │   ├── files/
│   │   │   ├── vars/
│   │   │   ├── defaults/
│   │   │   └── meta/
│   │   ├── backend/
│   │   ├── frontend/
│   │   ├── player/
│   │   ├── database/
│   │   ├── monitoring/
│   │   ├── security/
│   │   └── backup/
│   │
│   ├── group_vars/          # Variables por grupo
│   │   ├── all.yml
│   │   ├── backend.yml
│   │   ├── frontend.yml
│   │   ├── players.yml
│   │   └── monitoring.yml
│   │
│   ├── host_vars/           # Variables por host
│   │   └── example-host.yml
│   │
│   └── files/               # Archivos estáticos
│       ├── ssl/
│       ├── configs/
│       └── scripts/
│
├── kubernetes/              # ☸️ Configuración Kubernetes (futuro)
│   ├── namespace.yaml
│   ├── backend/
│   ├── frontend/
│   ├── monitoring/
│   └── ingress/
│
└── scripts/                 # 🛠️ Scripts de Automatización
    ├── deploy.sh            # Script principal de despliegue
    ├── setup-development.sh # Setup de entorno de desarrollo
    ├── backup-system.sh     # Backup completo del sistema
    ├── restore-system.sh    # Restauración del sistema
    ├── health-check.sh      # Health check de infraestructura
    ├── scale-up.sh          # Escalado hacia arriba
    ├── scale-down.sh        # Escalado hacia abajo
    ├── migrate-data.sh      # Migración de datos
    ├── update-certificates.sh # Actualización de certificados
    └── disaster-recovery.sh # Recuperación ante desastres
```

---

## 🧪 Tests (`/tests`) - Pruebas de Integración Global

### **Estructura de Testing Completa**
```
tests/
├── __init__.py
├── conftest.py              # Configuración global de pytest
├── pytest.ini              # Configuración de pytest
├── requirements.txt         # Dependencias específicas para testing
├── README.md               # Documentación de testing
│
├── fixtures/               # 📋 Datos de Prueba
│   ├── __init__.py
│   ├── videos/             # Videos de ejemplo para testing
│   │   ├── valid_10s.mp4   # Video válido de 10 segundos
│   │   ├── valid_20s.mp4   # Video válido de 20 segundos (límite)
│   │   ├── invalid_25s.mp4 # Video inválido de 25 segundos
│   │   ├── invalid_0s.mp4  # Video inválido de 0 segundos
│   │   ├── corrupted.mp4   # Video corrupto
│   │   ├── large_file.mp4  # Archivo muy grande (>100MB)
│   │   └── various_formats/ # Diferentes formatos de video
│   ├── configs/            # Configuraciones de prueba
│   │   ├── player_configs/
│   │   │   ├── basic.yaml
│   │   │   ├── high_performance.yaml
│   │   │   └── low_bandwidth.yaml
│   │   ├── backend_configs/
│   │   │   ├── test.env
│   │   │   └── integration.env
│   │   └── database/
│   │       ├── test_schema.sql
│   │       └── sample_data.sql
│   ├── api_responses/      # Respuestas de API mockadas
│   │   ├── auth_responses.json
│   │   ├── content_responses.json
│   │   ├── player_responses.json
│   │   └── error_responses.json
│   └── certificates/       # Certificados de prueba
│       ├── test_ca.crt
│       ├── test_server.crt
│       └── test_client.crt
│
├── unit/                   # 🔬 Pruebas Unitarias Específicas
│   ├── __init__.py
│   ├── backend/
│   │   ├── test_content_service.py    # ✅ Validación duración corregida
│   │   ├── test_storage_service.py    # ✅ Gestión de almacenamiento
│   │   ├── test_publish_service.py    # ✅ Concurrencia y locks
│   │   ├── test_auth_service.py
│   │   ├── test_schedule_service.py
│   │   └── test_metrics_service.py
│   ├── frontend/
│   │   ├── test_video_uploader.py     # ✅ Validación frontend 1-20s
│   │   ├── test_api_client.py
│   │   ├── test_auth_hooks.py
│   │   └── test_form_validation.py
│   ├── player/
│   │   ├── test_reconciler.py         # ✅ Reconciliación robusta
│   │   ├── test_storage_manager.py    # ✅ Gestión almacenamiento local
│   │   ├── test_network_manager.py    # ✅ Manejo de red con retry
│   │   ├── test_playlist_manager.py
│   │   └── test_monitoring_service.py
│   └── shared/
│       ├── test_sync_protocol.py
│       ├── test_validation_utils.py
│       └── test_crypto_utils.py
│
├── integration/            # 🔗 Pruebas de Integración
│   ├── __init__.py
│   ├── test_full_workflow.py          # ✅ Flujo completo: upload → schedule → sync
│   ├── test_multi_screen_sync.py      # ✅ Sincronización múltiples pantallas
│   ├── test_failure_recovery.py       # ✅ Recuperación de fallos críticos
│   ├── test_concurrent_operations.py  # ✅ Operaciones concurrentes
│   ├── test_storage_limits.py         # ✅ Límites de almacenamiento
│   ├── test_network_scenarios.py      # ✅ Escenarios de red
│   ├── test_authentication_flow.py    # Flujo completo de autenticación
│   ├── test_content_lifecycle.py      # Ciclo de vida del contenido
│   ├── test_schedule_resolution.py    # Resolución de programación
│   ├── test_player_provisioning.py    # Aprovisionamiento de players
│   ├── test_backup_restore.py         # Backup y restauración
│   └── test_api_compatibility.py      # Compatibilidad de APIs
│
├── e2e/                    # 🌍 Pruebas End-to-End
│   ├── __init__.py
│   ├── test_user_journey.py           # Viaje completo del usuario
│   ├── test_player_lifecycle.py       # Ciclo de vida completo del player
│   ├── test_content_distribution.py   # Distribución completa de contenido
│   ├── test_system_recovery.py        # Recuperación del sistema
│   ├── test_scaling_scenarios.py      # Escenarios de escalado
│   ├── test_maintenance_mode.py       # Modo de mantenimiento
│   └── browser/                       # Pruebas de navegador
│       ├── test_admin_interface.py    # Interfaz de administración
│       ├── test_upload_flow.py        # Flujo de subida de archivos
│       ├── test_scheduling_ui.py      # UI de programación
│       └── test_monitoring_dashboard.py # Dashboard de monitoreo
│
├── performance/            # 🚀 Pruebas de Rendimiento
│   ├── __init__.py
│   ├── test_load.py                   # Pruebas de carga normal
│   ├── test_stress.py                 # Pruebas de estrés
│   ├── test_scalability.py            # Pruebas de escalabilidad
│   ├── test_concurrency.py            # Concurrencia extrema
│   ├── test_large_files.py            # Archivos grandes
│   ├── test_many_players.py           # Muchos players simultáneos
│   ├── test_database_performance.py   # Rendimiento de base de datos
│   ├── test_network_bandwidth.py      # Uso de ancho de banda
│   └── benchmarks/                    # Benchmarks específicos
│       ├── upload_benchmark.py
│       ├── sync_benchmark.py
│       ├── database_benchmark.py
│       └── storage_benchmark.py
│
├── security/               # 🔒 Pruebas de Seguridad
│   ├── __init__.py
│   ├── test_authentication.py         # Seguridad de autenticación
│   ├── test_authorization.py          # Controles de autorización
│   ├── test_input_validation.py       # Validación de entrada
│   ├── test_file_upload_security.py   # Seguridad de subida de archivos
│   ├── test_api_security.py           # Seguridad de APIs
│   ├── test_player_security.py        # Seguridad del player
│   ├── test_data_encryption.py        # Encriptación de datos
│   ├── test_network_security.py       # Seguridad de red
│   └── vulnerability/                 # Tests de vulnerabilidades
│       ├── test_sql_injection.py
│       ├── test_xss_protection.py
│       ├── test_csrf_protection.py
│       └── test_file_traversal.py
│
├── chaos/                  # 🌪️ Chaos Engineering
│   ├── __init__.py
│   ├── test_network_failures.py       # Fallos de red aleatorios
│   ├── test_server_crashes.py         # Crashes del servidor
│   ├── test_database_failures.py      # Fallos de base de datos
│   ├── test_storage_failures.py       # Fallos de almacenamiento
│   ├── test_partial_deployments.py    # Despliegues parciales
│   ├── test_resource_exhaustion.py    # Agotamiento de recursos
│   └── scenarios/                     # Escenarios de caos
│       ├── network_partition.py
│       ├── high_latency.py
│       ├── packet_loss.py
│       └── resource_starvation.py
│
├── compatibility/          # 🔄 Pruebas de Compatibilidad
│   ├── __init__.py
│   ├── test_browser_compatibility.py  # Compatibilidad de navegadores
│   ├── test_device_compatibility.py   # Compatibilidad de dispositivos
│   ├── test_os_compatibility.py       # Compatibilidad de SO
│   ├── test_version_compatibility.py  # Compatibilidad de versiones
│   ├── test_api_versioning.py         # Versionado de API
│   └── matrix/                        # Matrices de compatibilidad
│       ├── browsers.yaml
│       ├── devices.yaml
│       └── operating_systems.yaml
│
├── regression/             # 🔄 Pruebas de Regresión
│   ├── __init__.py
│   ├── test_critical_paths.py         # Rutas críticas del sistema
│   ├── test_bug_fixes.py              # Verificación de bugs corregidos
│   ├── test_feature_stability.py      # Estabilidad de características
│   └── snapshots/                     # Snapshots para regresión
│       ├── api_responses/
│       ├── ui_screenshots/
│       └── database_states/
│
├── accessibility/          # ♿ Pruebas de Accesibilidad
│   ├── __init__.py
│   ├── test_wcag_compliance.py        # Cumplimiento WCAG
│   ├── test_keyboard_navigation.py    # Navegación por teclado
│   ├── test_screen_readers.py         # Lectores de pantalla
│   └── test_color_contrast.py         # Contraste de colores
│
├── monitoring/             # 📊 Pruebas de Monitoreo
│   ├── __init__.py
│   ├── test_metrics_collection.py     # Recolección de métricas
│   ├── test_alerting.py               # Sistema de alertas
│   ├── test_health_checks.py          # Health checks
│   ├── test_log_analysis.py           # Análisis de logs
│   └── test_dashboard_accuracy.py     # Precisión de dashboards
│
├── helpers/                # 🛠️ Helpers para Testing
│   ├── __init__.py
│   ├── api_helpers.py                 # Helpers para APIs
│   ├── database_helpers.py            # Helpers para base de datos
│   ├── file_helpers.py                # Helpers para archivos
│   ├── network_helpers.py             # Helpers para red
│   ├── player_simulator.py            # Simulador de players
│   ├── mock_server.py                 # Servidor mock
│   ├── test_data_generator.py         # Generador de datos
│   ├── assertion_helpers.py           # Assertions personalizadas
│   └── cleanup_helpers.py             # Helpers de limpieza
│
├── reports/                # 📋 Reportes de Testing
│   ├── coverage/                      # Reportes de cobertura
│   ├── performance/                   # Reportes de rendimiento
│   ├── security/                      # Reportes de seguridad
│   └── accessibility/                 # Reportes de accesibilidad
│
└── docker/                 # 🐳 Entornos de Testing
    ├── test-environment.yml           # Environment para testing
    ├── integration-tests.yml          # Environment para integración
    ├── performance-tests.yml          # Environment para performance
    └── mock-services/                 # Servicios mock
        ├── mock-tailscale/
        ├── mock-minio/
        └── mock-ffmpeg/
```

---

## 📊 Monitoring (`/monitoring`) - Observabilidad y Monitoreo

### **Estructura de Monitoreo Completa**
```
monitoring/
├── README.md               # Documentación de monitoreo
├── docker-compose.yml      # Stack completo de monitoreo
│
├── prometheus/             # 📈 Prometheus
│   ├── prometheus.yml      # Configuración principal
│   ├── rules/              # Reglas de alertas
│   │   ├── backend.yml     # Alertas del backend
│   │   ├── player.yml      # Alertas de players
│   │   ├── infrastructure.yml # Alertas de infraestructura
│   │   ├── business.yml    # Alertas de negocio
│   │   └── critical.yml    # Alertas críticas
│   ├── targets/            # Targets dinámicos
│   │   ├── backend_targets.json
│   │   ├── player_targets.json
│   │   └── infrastructure_targets.json
│   └── configs/            # Configuraciones por ambiente
│       ├── development.yml
│       ├── staging.yml
│       └── production.yml
│
├── grafana/                # 📊 Grafana
│   ├── grafana.ini         # Configuración principal
│   ├── provisioning/       # Configuración automática
│   │   ├── datasources/
│   │   │   ├── prometheus.yml
│   │   │   ├── loki.yml
│   │   │   └── postgres.yml
│   │   ├── dashboards/
│   │   │   └── dashboard.yml
│   │   └── notifiers/
│   │       ├── slack.yml
│   │       └── email.yml
│   ├── dashboards/         # Dashboards predefinidos
│   │   ├── system-overview.json       # Vista general del sistema
│   │   ├── backend-performance.json   # Rendimiento del backend
│   │   ├── player-metrics.json        # Métricas de players
│   │   ├── content-analytics.json     # Analytics de contenido
│   │   ├── network-monitoring.json    # Monitoreo de red
│   │   ├── storage-usage.json         # Uso de almacenamiento
│   │   ├── sync-performance.json      # Rendimiento de sincronización
│   │   ├── error-tracking.json        # Tracking de errores
│   │   ├── business-metrics.json      # Métricas de negocio
│   │   └── sla-monitoring.json        # Monitoreo de SLA
│   ├── plugins/            # Plugins personalizados
│   │   └── avtech-plugin/
│   └── themes/             # Temas personalizados
│       └── avtech-theme.json
│
├── alertmanager/           # 🚨 Alert Manager
│   ├── alertmanager.yml    # Configuración principal
│   ├── templates/          # Plantillas de alertas
│   │   ├── slack.tmpl      # Template para Slack
│   │   ├── email.tmpl      # Template para email
│   │   ├── webhook.tmpl    # Template para webhooks
│   │   └── pagerduty.tmpl  # Template para PagerDuty
│   ├── routing/            # Configuración de routing
│   │   ├── critical.yml    # Routing de alertas críticas
│   │   ├── warning.yml     # Routing de warnings
│   │   └── info.yml        # Routing informativo
│   └── inhibition/         # Reglas de inhibición
│       └── rules.yml
│
├── loki/                   # 📝 Loki (Logging)
│   ├── loki.yml            # Configuración principal
│   ├── rules/              # Reglas de logging
│   │   ├── backend_logs.yml
│   │   ├── player_logs.yml
│   │   └── system_logs.yml
│   └── retention/          # Políticas de retención
│       └── retention.yml
│
├── promtail/               # 📤 Promtail (Log Shipper)
│   ├── promtail.yml        # Configuración principal
│   ├── pipelines/          # Pipelines de procesamiento
│   │   ├── backend.yml     # Pipeline para logs del backend
│   │   ├── player.yml      # Pipeline para logs del player
│   │   ├── nginx.yml       # Pipeline para logs de Nginx
│   │   └── system.yml      # Pipeline para logs del sistema
│   └── targets/            # Targets de logs
│       ├── file_targets.yml
│       └── syslog_targets.yml
│
├── jaeger/                 # 🔍 Jaeger (Tracing)
│   ├── jaeger.yml          # Configuración principal
│   ├── sampling/           # Configuración de sampling
│   │   ├── strategies.json
│   │   └── operations.json
│   └── storage/            # Configuración de almacenamiento
│       └── elasticsearch.yml
│
├── elasticsearch/          # 🔎 Elasticsearch
│   ├── elasticsearch.yml   # Configuración principal
│   ├── mappings/           # Mappings de índices
│   │   ├── logs.json
│   │   ├── metrics.json
│   │   └── traces.json
│   ├── templates/          # Templates de índices
│   │   ├── logs_template.json
│   │   └── metrics_template.json
│   └── policies/           # Políticas de lifecycle
│       ├── logs_policy.json
│       └── metrics_policy.json
│
├── scripts/                # 🛠️ Scripts de Monitoreo
│   ├── setup-monitoring.sh         # Setup inicial
│   ├── backup-monitoring.sh        # Backup de configuraciones
│   ├── restore-monitoring.sh       # Restauración
│   ├── health-check.sh             # Health check del stack
│   ├── alert-test.sh               # Test de alertas
│   ├── dashboard-export.sh         # Export de dashboards
│   ├── dashboard-import.sh         # Import de dashboards
│   ├── metric-validation.py        # Validación de métricas
│   └── log-analysis.py             # Análisis de logs
│
├── exporters/              # 📊 Exporters Personalizados
│   ├── avtech-exporter/             # Exporter específico de AVTech
│   │   ├── main.py
│   │   ├── metrics.py
│   │   ├── config.py
│   │   └── Dockerfile
│   ├── player-exporter/             # Exporter para players
│   │   ├── main.py
│   │   ├── player_metrics.py
│   │   └── Dockerfile
│   └── business-exporter/           # Exporter de métricas de negocio
│       ├── main.py
│       ├── business_metrics.py
│       └── Dockerfile
│
├── synthetic/              # 🤖 Monitoreo Sintético
│   ├── uptime-checks/               # Checks de uptime
│   │   ├── api-health.py
│   │   ├── player-connectivity.py
│   │   └── service-availability.py
│   ├── performance-tests/           # Tests de rendimiento sintéticos
│   │   ├── api-response-time.py
│   │   ├── upload-performance.py
│   │   └── sync-latency.py
│   └── user-journeys/               # Viajes de usuario sintéticos
│       ├── login-flow.py
│       ├── upload-flow.py
│       └── scheduling-flow.py
│
├── runbooks/               # 📖 Runbooks Operacionales
│   ├── incident-response/           # Respuesta a incidentes
│   │   ├── high-cpu-usage.md
│   │   ├── database-slow-queries.md
│   │   ├── player-offline.md
│   │   ├── sync-failures.md
│   │   ├── storage-full.md
│   │   └── network-connectivity.md
│   ├── maintenance/                 # Procedimientos de mantenimiento
│   │   ├── backup-procedures.md
│   │   ├── update-procedures.md
│   │   ├── scaling-procedures.md
│   │   └── disaster-recovery.md
│   └── troubleshooting/             # Guías de troubleshooting
│       ├── common-issues.md
│       ├── performance-issues.md
│       ├── connectivity-issues.md
│       └── data-integrity.md
│
└── sla/                    # 📋 Service Level Agreements
    ├── sla-definitions.yml          # Definiciones de SLA
    ├── slo-targets.yml              # Objetivos de SLO
    ├── error-budgets.yml            # Presupuestos de error
    └── reports/                     # Reportes de SLA
        ├── monthly-sla-report.md
        ├── quarterly-review.md
        └── annual-summary.md
```

---

## 🔧 Tools (`/tools`) - Herramientas de Desarrollo

### **Estructura de Herramientas**
```
tools/
├── README.md               # Documentación de herramientas
│
├── db-viewer/              # 🗄️ Visor de Base de Datos
│   ├── app.py              # Aplicación web para ver BD
│   ├── queries/            # Queries predefinidas
│   │   ├── player_status.sql
│   │   ├── sync_history.sql
│   │   ├── storage_usage.sql
│   │   └── error_analysis.sql
│   ├── templates/          # Templates HTML
│   │   ├── index.html
│   │   ├── query_result.html
│   │   └── dashboard.html
│   ├── static/             # Assets estáticos
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── requirements.txt    # Dependencias
│
├── log-analyzer/           # 📋 Analizador de Logs
│   ├── analyzer.py         # Analizador principal
│   ├── parsers/            # Parsers por tipo de log
│   │   ├── backend_parser.py
│   │   ├── player_parser.py
│   │   ├── nginx_parser.py
│   │   └── system_parser.py
│   ├── patterns/           # Patrones de análisis
│   │   ├── error_patterns.py
│   │   ├── performance_patterns.py
│   │   └── security_patterns.py
│   ├── reports/            # Generadores de reportes
│   │   ├── error_report.py
│   │   ├── performance_report.py
│   │   └── summary_report.py
│   ├── config/             # Configuraciones
│   │   ├── analysis_config.yml
│   │   └── thresholds.yml
│   └── output/             # Reportes generados
│       ├── daily/
│       ├── weekly/
│       └── monthly/
│
├── player-simulator/       # 🎮 Simulador de Players
│   ├── simulator.py        # Simulador principal
│   ├── player_mock.py      # Mock de player individual
│   ├── network_simulator.py # Simulación de condiciones de red
│   ├── scenarios/          # Escenarios de simulación
│   │   ├── normal_operation.py     # Operación normal
│   │   ├── network_issues.py       # Problemas de red
│   │   ├── storage_full.py         # Almacenamiento lleno
│   │   ├── sync_conflicts.py       # Conflictos de sincronización
│   │   ├── mass_deployment.py      # Despliegue masivo
│   │   └── disaster_recovery.py    # Recuperación de desastres
│   ├── config/             # Configuraciones de simulación
│   │   ├── player_profiles.yml     # Perfiles de players
│   │   ├── network_profiles.yml    # Perfiles de red
│   │   └── test_scenarios.yml      # Escenarios de prueba
│   ├── reports/            # Reportes de simulación
│   │   ├── performance_report.py
│   │   ├── stress_test_report.py
│   │   └── scenario_report.py
│   └── utils/              # Utilidades del simulador
│       ├── metrics_collector.py
│       ├── load_generator.py
│       └── result_analyzer.py
│
├── data-generator/         # 🎲 Generador de Datos de Prueba
│   ├── generate_test_data.py       # Generador principal
│   ├── generators/                 # Generadores específicos
│   │   ├── user_generator.py       # Generación de usuarios
│   │   ├── content_generator.py    # Generación de contenido
│   │   ├── screen_generator.py     # Generación de pantallas
│   │   ├── schedule_generator.py   # Generación de programaciones
│   │   └── metrics_generator.py    # Generación de métricas
│   ├── templates/                  # Templates de datos
│   │   ├── user_templates.yml
│   │   ├── content_templates.yml
│   │   ├── screen_templates.yml
│   │   └── schedule_templates.yml
│   ├── datasets/                   # Datasets predefinidos
│   │   ├── small_dataset.yml       # Dataset pequeño (desarrollo)
│   │   ├── medium_dataset.yml      # Dataset mediano (testing)
│   │   ├── large_dataset.yml       # Dataset grande (performance)
│   │   └── stress_dataset.yml      # Dataset para stress testing
│   ├── validators/                 # Validadores de datos generados
│   │   ├── data_validator.py
│   │   ├── consistency_checker.py
│   │   └── integrity_validator.py
│   └── export/                     # Exportadores
│       ├── sql_exporter.py
│       ├── json_exporter.py
│       ├── csv_exporter.py
│       └── api_loader.py
│
├── performance-profiler/   # 📊 Profiler de Rendimiento
│   ├── profiler.py         # Profiler principal
│   ├── backend_profiler.py # Profiling del backend
│   ├── player_profiler.py  # Profiling del player
│   ├── database_profiler.py # Profiling de base de datos
│   ├── memory_profiler.py  # Profiling de memoria
│   ├── cpu_profiler.py     # Profiling de CPU
│   ├── io_profiler.py      # Profiling de I/O
│   ├── network_profiler.py # Profiling de red
│   ├── reports/            # Reportes de profiling
│   │   ├── performance_report.py
│   │   ├── bottleneck_analysis.py
│   │   └── optimization_suggestions.py
│   └── config/             # Configuración de profiling
│       ├── profiling_config.yml
│       └── thresholds.yml
│
├── api-tester/             # 🔌 Tester de APIs
│   ├── api_tester.py       # Tester principal
│   ├── test_suites/        # Suites de testing
│   │   ├── auth_tests.py   # Tests de autenticación
│   │   ├── content_tests.py # Tests de contenido
│   │   ├── player_tests.py # Tests de player API
│   │   ├── admin_tests.py  # Tests de administración
│   │   └── integration_tests.py # Tests de integración
│   ├── scenarios/          # Escenarios de testing
│   │   ├── load_scenarios.py
│   │   ├── stress_scenarios.py
│   │   ├── error_scenarios.py
│   │   └── edge_case_scenarios.py
│   ├── config/             # Configuración de tests
│   │   ├── api_config.yml
│   │   ├── test_data.yml
│   │   └── environments.yml
│   ├── reports/            # Reportes de testing
│   │   ├── test_results.py
│   │   ├── performance_metrics.py
│   │   └── coverage_report.py
│   └── utils/              # Utilidades de testing
│       ├── request_builder.py
│       ├── response_validator.py
│       ├── assertion_helper.py
│       └── mock_server.py
│
├── deployment-helper/      # 🚀 Helper de Despliegue
│   ├── deploy_helper.py    # Helper principal
│   ├── environment_setup.py # Setup de ambientes
│   ├── config_validator.py # Validador de configuraciones
│   ├── health_checker.py   # Verificador de salud post-deploy
│   ├── rollback_manager.py # Gestor de rollback
│   ├── migration_runner.py # Ejecutor de migraciones
│   ├── service_manager.py  # Gestor de servicios
│   ├── templates/          # Templates de configuración
│   │   ├── nginx.conf.j2
│   │   ├── systemd.service.j2
│   │   ├── docker-compose.yml.j2
│   │   ├── env.template
│   │   └── database.conf.j2
│   ├── validators/         # Validadores específicos
│   │   ├── config_validator.py
│   │   ├── dependency_checker.py
│   │   ├── port_checker.py
│   │   └── permission_checker.py
│   ├── scripts/            # Scripts auxiliares
│   │   ├── pre_deploy.sh
│   │   ├── post_deploy.sh
│   │   ├── health_check.sh
│   │   └── cleanup.sh
│   └── playbooks/          # Playbooks de Ansible
│       ├── setup.yml
│       ├── deploy.yml
│       ├── rollback.yml
│       └── maintenance.yml
│
├── security-scanner/       # 🔒 Scanner de Seguridad
│   ├── scanner.py          # Scanner principal
│   ├── vulnerability_scanner.py # Scanner de vulnerabilidades
│   ├── dependency_checker.py   # Checker de dependencias
│   ├── config_auditor.py       # Auditor de configuraciones
│   ├── permission_auditor.py   # Auditor de permisos
│   ├── network_scanner.py      # Scanner de red
│   ├── file_integrity_checker.py # Checker de integridad
│   ├── rules/              # Reglas de seguridad
│   │   ├── owasp_rules.yml
│   │   ├── custom_rules.yml
│   │   ├── compliance_rules.yml
│   │   └── best_practices.yml
│   ├── reports/            # Reportes de seguridad
│   │   ├── vulnerability_report.py
│   │   ├── compliance_report.py
│   │   ├── risk_assessment.py
│   │   └── remediation_plan.py
│   └── config/             # Configuración del scanner
│       ├── scanner_config.yml
│       ├── severity_levels.yml
│       └── exclusions.yml
│
├── backup-restore/         # 💾 Herramientas de Backup y Restore
│   ├── backup_manager.py   # Gestor principal de backup
│   ├── database_backup.py  # Backup de base de datos
│   ├── file_backup.py      # Backup de archivos
│   ├── config_backup.py    # Backup de configuraciones
│   ├── restore_manager.py  # Gestor de restauración
│   ├── incremental_backup.py # Backup incremental
│   ├── compression_manager.py # Gestor de compresión
│   ├── encryption_manager.py  # Gestor de encriptación
│   ├── schedules/          # Programaciones de backup
│   │   ├── daily_backup.yml
│   │   ├── weekly_backup.yml
│   │   ├── monthly_backup.yml
│   │   └── disaster_recovery.yml
│   ├── strategies/         # Estrategias de backup
│   │   ├── full_backup_strategy.py
│   │   ├── incremental_strategy.py
│   │   ├── differential_strategy.py
│   │   └── snapshot_strategy.py
│   ├── validators/         # Validadores de backup
│   │   ├── backup_validator.py
│   │   ├── integrity_checker.py
│   │   └── restore_tester.py
│   └── reports/            # Reportes de backup
│       ├── backup_status.py
│       ├── recovery_time.py
│       └── storage_usage.py
│
├── migration-tools/        # 🔄 Herramientas de Migración
│   ├── migration_manager.py    # Gestor principal
│   ├── data_migrator.py        # Migración de datos
│   ├── schema_migrator.py      # Migración de esquemas
│   ├── config_migrator.py      # Migración de configuraciones
│   ├── version_migrator.py     # Migración entre versiones
│   ├── bulk_migrator.py        # Migración masiva
│   ├── rollback_manager.py     # Gestor de rollback
│   ├── scripts/                # Scripts de migración
│   │   ├── v1_to_v2.py
│   │   ├── legacy_import.py
│   │   ├── bulk_import.py
│   │   └── data_cleanup.py
│   ├── validators/             # Validadores de migración
│   │   ├── pre_migration_check.py
│   │   ├── post_migration_check.py
│   │   ├── data_integrity_check.py
│   │   └── consistency_check.py
│   ├── templates/              # Templates de migración
│   │   ├── migration_template.py
│   │   ├── rollback_template.py
│   │   └── validation_template.py
│   └── reports/                # Reportes de migración
│       ├── migration_status.py
│       ├── performance_report.py
│       └── error_summary.py
│
├── load-testing/           # 🚀 Herramientas de Load Testing
│   ├── load_tester.py      # Tester principal
│   ├── scenario_runner.py  # Ejecutor de escenarios
│   ├── metrics_collector.py # Recolector de métricas
│   ├── report_generator.py # Generador de reportes
│   ├── scenarios/          # Escenarios de carga
│   │   ├── normal_load.py  # Carga normal
│   │   ├── peak_load.py    # Carga pico
│   │   ├── stress_load.py  # Carga de estrés
│   │   ├── spike_load.py   # Carga de picos
│   │   ├── endurance_load.py # Carga de resistencia
│   │   └── capacity_load.py  # Carga de capacidad
│   ├── profiles/           # Perfiles de usuario
│   │   ├── admin_profile.py
│   │   ├── content_manager_profile.py
│   │   ├── viewer_profile.py
│   │   └── api_client_profile.py
│   ├── config/             # Configuración de load testing
│   │   ├── load_config.yml
│   │   ├── thresholds.yml
│   │   └── environments.yml
│   ├── reports/            # Reportes de carga
│   │   ├── performance_summary.py
│   │   ├── bottleneck_analysis.py
│   │   ├── scalability_report.py
│   │   └── recommendation_report.py
│   └── utils/              # Utilidades de load testing
│       ├── request_generator.py
│       ├── data_generator.py
│       ├── session_manager.py
│       └── result_analyzer.py
│
├── documentation-generator/ # 📖 Generador de Documentación
│   ├── doc_generator.py    # Generador principal
│   ├── api_doc_generator.py # Generador de docs de API
│   ├── code_doc_generator.py # Generador de docs de código
│   ├── database_doc_generator.py # Generador de docs de BD
│   ├── architecture_doc_generator.py # Generador de docs de arquitectura
│   ├── runbook_generator.py # Generador de runbooks
│   ├── templates/          # Templates de documentación
│   │   ├── api_template.md
│   │   ├── readme_template.md
│   │   ├── runbook_template.md
│   │   ├── architecture_template.md
│   │   └── changelog_template.md
│   ├── parsers/            # Parsers de código
│   │   ├── python_parser.py
│   │   ├── typescript_parser.py
│   │   ├── sql_parser.py
│   │   └── yaml_parser.py
│   ├── extractors/         # Extractores de información
│   │   ├── comment_extractor.py
│   │   ├── docstring_extractor.py
│   │   ├── annotation_extractor.py
│   │   └── schema_extractor.py
│   ├── formatters/         # Formateadores de output
│   │   ├── markdown_formatter.py
│   │   ├── html_formatter.py
│   │   ├── pdf_formatter.py
│   │   └── wiki_formatter.py
│   └── config/             # Configuración del generador
│       ├── doc_config.yml
│       ├── style_config.yml
│       └── output_config.yml
│
└── dev-utilities/          # 🛠️ Utilidades de Desarrollo
    ├── code_generator/     # Generador de código
    │   ├── generator.py
    │   ├── model_generator.py
    │   ├── api_generator.py
    │   ├── test_generator.py
    │   ├── migration_generator.py
    │   └── templates/
    │       ├── model_template.py
    │       ├── api_template.py
    │       ├── test_template.py
    │       └── migration_template.py
    │
    ├── dependency_analyzer/ # Analizador de dependencias
    │   ├── analyzer.py
    │   ├── python_analyzer.py
    │   ├── nodejs_analyzer.py
    │   ├── security_analyzer.py
    │   ├── license_analyzer.py
    │   └── reports/
    │       ├── dependency_report.py
    │       ├── security_report.py
    │       └── license_report.py
    │
    ├── code_quality/       # Herramientas de calidad de código
    │   ├── quality_checker.py
    │   ├── complexity_analyzer.py
    │   ├── duplication_detector.py
    │   ├── style_checker.py
    │   ├── security_scanner.py
    │   └── reports/
    │       ├── quality_report.py
    │       ├── complexity_report.py
    │       └── security_report.py
    │
    ├── environment_manager/ # Gestor de ambientes
    │   ├── env_manager.py
    │   ├── docker_manager.py
    │   ├── venv_manager.py
    │   ├── config_manager.py
    │   └── scripts/
    │       ├── setup_dev.sh
    │       ├── setup_test.sh
    │       ├── setup_prod.sh
    │       └── cleanup.sh
    │
    ├── git_hooks/          # Git hooks personalizados
    │   ├── pre-commit      # Hook pre-commit
    │   ├── pre-push        # Hook pre-push
    │   ├── commit-msg      # Hook commit-msg
    │   ├── post-merge      # Hook post-merge
    │   └── scripts/
    │       ├── run_tests.py
    │       ├── check_style.py
    │       ├── check_security.py
    │       └── update_docs.py
    │
    └── project_manager/    # Gestor de proyecto
        ├── project_manager.py
        ├── task_manager.py
        ├── milestone_tracker.py
        ├── progress_reporter.py
        ├── time_tracker.py
        └── reports/
            ├── progress_report.py
            ├── velocity_report.py
            ├── burndown_chart.py
            └── team_productivity.py
```

---

## 📋 Archivos de Configuración Raíz

### **Archivos Principales en la Raíz del Proyecto**
```
avtech-platform/
├── .env                    # Variables de entorno principales
├── .env.example           # Plantilla de variables de entorno
├── .gitignore            # Archivos ignorados por Git
├── .gitattributes        # Atributos de Git
├── .dockerignore         # Archivos ignorados por Docker
├── .editorconfig         # Configuración del editor
├── .pre-commit-config.yaml # Configuración de pre-commit hooks
├── README.md             # Documentación principal del proyecto
├── CONTRIBUTING.md       # Guía de contribución
├── CHANGELOG.md          # Registro de cambios
├── LICENSE              # Licencia del proyecto
├── CODE_OF_CONDUCT.md   # Código de conducta
├── SECURITY.md          # Política de seguridad
│
├── Makefile             # Comandos principales del proyecto
├── docker-compose.yml   # Compose para producción
├── docker-compose.dev.yml # Compose para desarrollo
├── docker-compose.test.yml # Compose para testing
├── docker-compose.monitoring.yml # Compose para monitoreo
│
├── pyproject.toml       # Configuración Python del workspace
├── package.json         # Configuración Node.js del workspace
├── requirements.txt     # Dependencias Python del workspace
├── .python-version      # Versión de Python
├── .node-version        # Versión de Node.js
│
├── renovate.json        # Configuración de Renovate (dependencias)
├── dependabot.yml       # Configuración de Dependabot
├── .github/             # Configuración de GitHub
│   ├── workflows/       # GitHub Actions
│   │   ├── ci.yml       # Integración continua
│   │   ├── cd.yml       # Despliegue continuo
│   │   ├── security.yml # Análisis de seguridad
│   │   ├── docs.yml     # Generación de documentación
│   │   └── release.yml  # Proceso de release
│   ├── ISSUE_TEMPLATE/  # Templates de issues
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── security_report.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── CODEOWNERS       # Propietarios de código
│
└── config/              # Configuraciones globales
    ├── global.yml       # Configuración global
    ├── environments/    # Configuraciones por ambiente
    │   ├── development.yml
    │   ├── staging.yml
    │   ├── production.yml
    │   └── testing.yml
    ├── security/        # Configuraciones de seguridad
    │   ├── security.yml
    │   ├── cors.yml
    │   └── rate_limits.yml
    └── monitoring/      # Configuraciones de monitoreo
        ├── metrics.yml
        ├── alerts.yml
        └── dashboards.yml
```

---

## 🚀 Comandos Principales del Makefile

### **Makefile Ejemplo**
```makefile
# Comandos de desarrollo
.PHONY: dev setup test build deploy clean

# Variables
COMPOSE_FILE = docker-compose.dev.yml
BACKEND_DIR = backend
FRONTEND_DIR = frontend
PLAYER_DIR = player

# Comandos principales
dev: setup
	@echo "🚀 Iniciando entorno de desarrollo..."
	docker-compose -f $(COMPOSE_FILE) up -d
	make backend-dev &
	make frontend-dev &

setup:
	@echo "📦 Configurando entorno de desarrollo..."
	./scripts/setup-dev.sh

backend-dev:
	@echo "🖥️ Iniciando backend..."
	cd $(BACKEND_DIR) && ./run-dev.sh

frontend-dev:
	@echo "🌐 Iniciando frontend..."
	cd $(FRONTEND_DIR) && npm run dev

test:
	@echo "🧪 Ejecutando tests..."
	make test-backend
	make test-frontend
	make test-player
	make test-integration

test-backend:
	cd $(BACKEND_DIR) && pytest

test-frontend:
	cd $(FRONTEND_DIR) && npm test

test-player:
	cd $(PLAYER_DIR) && pytest

test-integration:
	cd tests && pytest integration/

build:
	@echo "🏗️ Construyendo aplicaciones..."
	docker-compose build

deploy-staging:
	@echo "🚀 Desplegando a staging..."
	./scripts/deploy.sh staging

deploy-production:
	@echo "🚀 Desplegando a producción..."
	./scripts/deploy.sh production

clean:
	@echo "🧹 Limpiando entorno..."
	docker-compose down -v
	docker system prune -f

migrate:
	@echo "📊 Ejecutando migraciones..."
	cd $(BACKEND_DIR) && python migrate.py

backup:
	@echo "💾 Creando backup..."
	./scripts/backup-db.sh

restore:
	@echo "🔄 Restaurando backup..."
	./scripts/restore-db.sh

logs:
	docker-compose logs -f

monitoring:
	@echo "📊 Iniciando stack de monitoreo..."
	docker-compose -f monitoring/docker-compose.yml up -d

security-scan:
	@echo "🔒 Ejecutando análisis de seguridad..."
	./tools/security-scanner/scanner.py

performance-test:
	@echo "⚡ Ejecutando tests de rendimiento..."
	./tools/load-testing/load_tester.py

docs:
	@echo "📖 Generando documentación..."
	./tools/documentation-generator/doc_generator.py

help:
	@echo "📋 Comandos disponibles:"
	@echo "  dev              - Iniciar entorno de desarrollo"
	@echo "  setup            - Configurar entorno"
	@echo "  test             - Ejecutar todos los tests"
	@echo "  build            - Construir aplicaciones"
	@echo "  deploy-staging   - Desplegar a staging"
	@echo "  deploy-production- Desplegar a producción"
	@echo "  clean            - Limpiar entorno"
	@echo "  migrate          - Ejecutar migraciones"
	@echo "  backup           - Crear backup"
	@echo "  restore          - Restaurar backup"
	@echo "  logs             - Ver logs"
	@echo "  monitoring       - Iniciar monitoreo"
	@echo "  security-scan    - Análisis de seguridad"
	@echo "  performance-test - Tests de rendimiento"
	@echo "  docs             - Generar documentación"
```

---

## 📝 Resumen de la Estructura

Esta estructura de directorios detallada para AVTech Platform proporciona:

### **🎯 Características Principales:**

1. **Separación Clara de Responsabilidades**: Cada directorio tiene un propósito específico y bien definido
2. **Escalabilidad**: La estructura soporta el crecimiento del proyecto sin problemas
3. **Mantenibilidad**: Código organizado y fácil de mantener
4. **Testing Completo**: Múltiples niveles de testing (unitario, integración, E2E, performance)
5. **Observabilidad Total**: Monitoreo, logging, métricas y alertas integradas
6. **Operaciones Automatizadas**: Scripts, herramientas y automatización para operaciones
7. **Desarrollo Eficiente**: Herramientas que aceleran el desarrollo y mantienen calidad

### **🔧 Correcciones Críticas Implementadas:**

1. ✅ **Validación de duración corregida** (1-20 segundos) en frontend y backend
2. ✅ **Gestión robusta de almacenamiento** con limpieza automática
3. ✅ **Reconciliación robusta** con manejo de errores y backoff exponencial
4. ✅ **Manejo de concurrencia** con locks y versionado optimista
5. ✅ **Observabilidad completa** con métricas, logging y alertas
6. ✅ **Testing exhaustivo** incluyendo escenarios de fallo
7. ✅ **Documentación operacional** con runbooks para incidentes

### **🚀 Beneficios de esta Estructura:**

- **Desarrollo Rápido**: Setup automatizado y herramientas de desarrollo
- **Calidad Asegurada**: Testing multicapa y herramientas de calidad
- **Operación Confiable**: Monitoreo proactivo y procedimientos de respuesta
- **Escalabilidad**: Arquitectura preparada para crecimiento
- **Mantenibilidad**: Código bien organizado y documentado
- **Seguridad**: Análisis de seguridad integrado y mejores prácticas

Esta estructura sirve como base sólida para implementar el proyecto AVTech con todas las correcciones críticas y mejores prácticas de la industria.