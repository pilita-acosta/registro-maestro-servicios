# Decisiones técnicas

## Alcance

El problema principal no es liquidar una factura, sino recuperar información confiable y mantenerla actualizada. El objeto central es el `Punto de Servicio`; las facturas y documentos son su historial.

## Arquitectura elegida

```text
Navegador / PWA móvil
          |
          v
Next.js (web responsive)
          |
          v
FastAPI (REST + OpenAPI)
          |
          +--> PostgreSQL (datos estructurados e historial)
          |
          +--> S3/MinIO (originales y PDFs)
```

### Por qué esta combinación

- Next.js permite una única interfaz para escritorio y teléfono, con buen soporte para formularios, búsquedas y PWA.
- TypeScript reduce errores en los datos que viajan entre pantallas y API.
- FastAPI encaja bien con importaciones, validaciones y procesamiento de archivos, y genera documentación de API automáticamente.
- PostgreSQL maneja relaciones, restricciones, búsquedas e historial mejor que un Excel compartido.
- S3/MinIO separa los archivos pesados de los datos consultables y permite conservar el original.

## Modelo inicial

```text
Dependencia 1---N PuntoServicio 1---N Cuenta 1---N Factura
Proveedor 1---N Cuenta
PuntoServicio 1---N RegistroDocumentacion 1---N Documento
RegistroDocumentacion 1---N MovimientoDocumentacion
```

`PuntoServicio` debe tener un identificador interno estable. NIS, número de cuenta y códigos externos son datos del proveedor y no deben usarse como clave principal.

## Reglas de calidad

1. Catálogos para dependencias, proveedores, tipos de servicio y estados.
2. Campos obligatorios validados antes de guardar.
3. No borrar físicamente datos maestros: se desactivan y se conserva el motivo.
4. Todo archivo recibido se conserva con fecha, origen y checksum.
5. Los cambios relevantes registran usuario, fecha, valor anterior y valor nuevo.
6. Las importaciones de Excel pasan por una vista de errores antes de confirmar.

## Evolución

1. MVP: búsqueda y padrón maestro.
2. Importación validada desde Excel y auditoría.
3. Facturas, documentos y trazabilidad entre oficinas.
4. Reportes de gasto e integración con sistemas institucionales.
