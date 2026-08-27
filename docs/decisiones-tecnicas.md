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

## Modelo inicial revisado

```text
Secretaria 1---N Dependencia 1---N Domicilio
Domicilio 1---N PuntoServicio 1---N Cuenta
Proveedor 1---N Contrato 1---N Cuenta
Servicio 1---N Contrato
Cuenta 1---N Factura 1---N Pago
Factura 1---N Imputacion N---1 Secretaria
PuntoServicio 1---N RegistroDocumentacion 1---N Documento
RegistroDocumentacion 1---N MovimientoDocumentacion
Contrato 1---N Conciliacion
```

`PuntoServicio`, `Cuenta`, `Contrato`, `Factura`, `Pago` e `Importacion` deben tener identificadores internos estables. NIS, número de cuenta, medidor y códigos externos son datos del proveedor y no deben usarse como clave principal.

### Distinción obligatoria

- `Domicilio`: dónde está el lugar.
- `Dependencia`: qué unidad municipal funciona allí.
- `PuntoServicio`: qué boca o relación de servicio se controla.
- `Cuenta`: cómo identifica esa boca el proveedor.
- `Contrato`: bajo qué condiciones se espera que facture.

Esta separación permite tener múltiples proveedores para un mismo domicilio y comparar lo recibido contra lo que contractualmente se esperaba recibir.

## Reglas de calidad

1. Catálogos para secretarías, dependencias, proveedores, tipos de servicio, frecuencias, estados y motivos.
2. Campos obligatorios validados antes de guardar.
3. No borrar físicamente datos maestros: se desactivan y se conserva el motivo.
4. Todo archivo recibido se conserva con fecha, origen y checksum.
5. Los cambios relevantes registran usuario, fecha, valor anterior y valor nuevo.
6. Las importaciones de Excel pasan por una vista de errores antes de confirmar.
7. Los contratos activos generan períodos esperados para conciliación.
8. La factura no se considera correctamente validada hasta que su boca, cuenta, período e imputación estén controlados.

## Evolución

1. MVP: ABM de catálogos, domicilios, dependencias y bocas de servicio.
2. Contratos, cuentas y calendario esperado de facturación.
3. Importación validada desde Excel y conciliación de faltantes/novedades.
4. Facturas, imputaciones, pagos, documentos y auditoría.
5. Reportes de gasto e integración con sistemas institucionales.
6. IA asistida para análisis, alertas y explicación de variaciones.
