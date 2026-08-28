# Registro Maestro de Servicios Municipales

Sistema para centralizar y consultar la información de los puntos de servicio municipales.

## Objetivo del primer MVP

- Buscar rápidamente por NIS, proveedor, dependencia, domicilio o cuenta.
- Mantener un registro único de puntos de servicio.
- Evitar nombres libres para dependencias y proveedores mediante catálogos.
- Conservar el historial de facturas y movimientos documentales.
- Permitir importar información existente desde Excel sin destruir los archivos originales.

## Decisiones iniciales

- **Frontend y experiencia web/mobile:** Next.js + TypeScript, responsive y PWA.
- **Backend y API:** FastAPI + Python, API REST documentada con OpenAPI.
- **Base de datos:** PostgreSQL 16.
- **Archivos originales y PDFs:** almacenamiento compatible con S3 (MinIO en desarrollo).
- **Despliegue:** Docker Compose en desarrollo; contenedores en un servidor Linux institucional o VPS en producción.
- **Autenticación:** usuarios institucionales mediante OIDC cuando exista proveedor; fallback local solo para desarrollo.

La aplicación móvil será inicialmente la misma PWA responsive. Esto reduce costo y duplicación; una app nativa se evaluará únicamente si aparece una necesidad real de cámara, trabajo offline o notificaciones push.

## Estructura

```text
apps/web       Frontend Next.js
apps/api       Backend FastAPI
docs            Decisiones, modelo y procedimiento operativo
infra           Docker y configuración de servicios
```

El flujo de ramas y validación está documentado en [docs/flujo-git.md](docs/flujo-git.md). El desarrollo actual se realiza en `feature/mvp-padron`; la integración a `main` queda sujeta a revisión.

## Ejecutar todo con Docker

Requiere Docker Desktop en Windows, macOS o Linux:

```powershell
docker compose -f infra/docker-compose.yml up --build
```

La aplicación web queda disponible en `http://localhost:3000`, la API en `http://localhost:8000/docs` y MinIO en `http://localhost:9001`. PostgreSQL queda disponible únicamente para los servicios del Compose en el puerto `5432`.

Para detener los servicios:

```powershell
docker compose -f infra/docker-compose.yml down
```

## Verificaciones automáticas

El build de `web` valida TypeScript durante la construcción. Las pruebas de la API usan una base SQLite temporal, por lo que no modifican PostgreSQL ni los datos de desarrollo:

```powershell
docker compose -f infra/docker-compose.yml --profile test run --rm api-tests
docker compose -f infra/docker-compose.yml --profile test run --rm ux-tests
docker compose -f infra/docker-compose.yml build web
```

Las pruebas de API cubren disponibilidad, resumen, columnas y filtros del Padrón, detalle del punto de servicio y el circuito de recepción, liquidación, pago y auditoría de una factura.

Las pruebas UX/UI validan navegación de escritorio y móvil, búsqueda en el Padrón, columnas visibles de la grilla y apertura de la ficha de un punto de servicio.

## Módulos funcionales previstos

- **Padrón maestro:** búsqueda y ficha de puntos de servicio.
- **ABM:** puntos de servicio, proveedores, servicios, cuentas, dependencias y secretarías.
- **Asignaciones:** relación punto de servicio-secretaría, con vigencia e historial.
- **Facturación:** carga manual, importación masiva, validación y consulta de facturas mensuales.
- **Pagos:** estado de pago, fecha, comprobante, importe pagado e imputación presupuestaria.
- **Documentación:** originales recibidos, documentos asociados y movimientos entre oficinas.
- **Dashboard:** gasto por período, proveedor, servicio, secretaría y estado de pago.
- **Importaciones:** perfiles por proveedor para transformar archivos Excel/CSV con columnas diferentes, previsualizar errores y confirmar lotes.

## Preguntas que debe resolver el MVP

- ¿Este servicio está pago?
- ¿Qué proveedor tiene este punto de servicio?
- ¿Se pagó esta factura?
- ¿Qué facturas de una lista están pagadas o pendientes?
- ¿Cuánto se gastó por servicio, proveedor, secretaría o dependencia?

El primer corte funcional será el padrón maestro con ABM, búsqueda e importación validada de facturas. Los pagos y el dashboard se incorporan sobre esa misma base histórica.

## Principio operativo

El archivo recibido nunca se modifica. Se guarda el original, se trabaja sobre una copia o importación validada y toda modificación de datos maestros queda auditada.
