# Decisiones técnicas

## Alcance

El objetivo principal es liquidar facturas de servicios a tiempo y evitar cortes. El `Punto de Servicio` es el contexto que permite identificar cada obligación, pero la factura, su control, su imputación y su resolución económica son el flujo central del MVP.

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
Secretaria 1---N Dependencia N---N Domicilio
Domicilio 1---N InmuebleAlquilado 1---N ContratoAlquiler
Domicilio 1---N PuntoServicio 1---N Cuenta
Proveedor 1---N Contrato 1---N Cuenta
PersonaEntidad 1---N PropietarioAlquiler
Proveedor 1---N LineaTelefonica 1---N DispositivoMovil
NotaPedido 1---1 ExpedienteCompra 1---N DispositivoMovil
DispositivoMovil 1---1 RegistroPatrimonial
LineaTelefonica 1---N IncidenciaTelefonia
Servicio 1---N Contrato
Contrato 1---1 Expediente 1---N Alcance 1---N Liquidacion
Liquidacion N---N Factura 1---N Pago
Factura 1---N ResolucionPago N---1 DestinatarioPago
ResolucionPago N---1 ModalidadLiquidacion
Liquidacion 1---N LiquidacionDetalle N---1 Cuenta
LiquidacionDetalle N---1 Secretaria
Alcance 1---N OrdenPago
Expediente 1---N UbicacionExpediente
Cuenta 1---N Factura
Factura 1---N Imputacion N---1 Secretaria
PuntoServicio 1---N RegistroDocumentacion 1---N Documento
RegistroDocumentacion 1---N MovimientoDocumentacion
Contrato 1---N Conciliacion
```

`PuntoServicio`, `Cuenta`, `Contrato`, `Factura`, `Pago` e `Importacion` deben tener identificadores internos estables. NIS, número de cuenta, medidor y códigos externos son datos del proveedor y no deben usarse como clave principal. La relación histórica entre dependencia y domicilio también debe tener un identificador propio y vigencia.

### Distinción obligatoria

- `Domicilio`: dónde está el lugar y qué dependencias lo ocuparon en cada período.
- `Dependencia`: qué unidad municipal del organigrama funciona o funcionó allí.
- `PuntoServicio`: qué boca o relación de servicio se controla.
- `Cuenta`: cómo identifica esa boca el proveedor.
- `Contrato`: bajo qué condiciones se espera que facture.
- `InmuebleAlquilado`: inmueble ocupado por alquiler, con propietario y expediente de alquiler propios.
- `Factura`: documento y obligación que debe controlarse, independientemente de quién la presenta o recibe el pago.
- `DestinatarioPago`: persona o entidad que recibe efectivamente el dinero.
- `ModalidadLiquidacion`: mecanismo usado para resolver el gasto, que puede ser pago directo, reintegro, pago al propietario o compensación.

Esta separación permite tener múltiples secretarías y proveedores en un mismo domicilio, conservar mudanzas y comparar lo recibido contra lo que contractualmente se esperaba recibir.

Todos los inmuebles alquilados del universo de Servicios pueden ser puntos de servicio. `uso` es una descripción funcional del inmueble y sirve para consulta, pero no determina por sí solo la imputación. La imputación se obtiene de la dependencia y su asignación vigente, con posibilidad de distribución múltiple cuando corresponda.

El sistema debe generar una bandeja de facturas esperadas y faltantes. La ausencia de una factura es un evento operativo: debe tener fecha límite, responsable de entrega, estado de reclamo, próximos pasos y riesgo de corte. Esta bandeja es más importante que una simple búsqueda histórica porque permite actuar antes de que venza la obligación.

La modalidad por defecto será `reintegro_mes_vencido`. `compensacion_proveedor` será una modalidad alternativa para los servicios incluidos en resúmenes de proveedores como ABSA, EDELAP o Camuzzi. Ambas pasan por el mismo control de facturación y documentación; solo cambia la forma posterior de resolver el gasto.

La telefonía móvil se modela como un módulo transversal. `LineaTelefonica` representa el servicio contratado y `DispositivoMovil` representa el bien físico. El vínculo entre ambos debe tener vigencia para permitir cambios de equipo, reasignaciones y líneas temporalmente sin dispositivo.

Las notas de pedido y expedientes de compra son referencias administrativas relacionadas con la adquisición, no sustitutos del registro patrimonial. El sistema conserva sus números, fechas, estados y vínculos con los dispositivos recibidos, dejando el alta patrimonial y sus movimientos bajo responsabilidad de la oficina de Patrimonio.

Las incidencias se almacenan como historial, no como una simple observación en la línea. Una incidencia puede cambiar de estado, tener intercambios con el proveedor y quedar vinculada a una factura, línea, IMEI, nota de pedido o expediente.

El proveedor del servicio, el titular o presentante del documento y el destinatario del pago son roles separados sobre una `PersonaEntidad`. El propietario de un inmueble alquilado puede recibir un reintegro o actuar como contraparte administrativa sin convertirse por eso en el proveedor técnico de agua, electricidad, gas o internet.

La resolución económica se registra después de validar la factura. Puede haber más de una resolución para una factura, por ejemplo un pago parcial y luego un saldo, pero el total resuelto debe poder conciliarse con el importe validado. Una compensación debe registrar resumen o comprobante, obligación compensada, período, importe y saldo resultante.

Una `LiquidacionGlobal` se implementará como una liquidación con muchos detalles, no como una factura gigante. `LiquidacionDetalle` conservará la fila de origen, factura, cuenta, boca, secretaría, importe informado, importe validado, estado y motivo de observación. Así se puede sumar por secretaría sin perder el nivel de detalle.

### Sistemas externos

`Expedientes` y `RAFAM` se tratan como sistemas de referencia externos. En la primera versión no se asume integración automática: el usuario carga o importa los números y el sistema valida formato, duplicidad y coherencia de relaciones. Más adelante se puede agregar una integración oficial si esos sistemas exponen API o intercambio de archivos.

El modelo debe conservar tanto el identificador estructurado como el texto original, por ejemplo:

- expediente normalizado: organismo, número, año;
- alcance: número y expediente padre;
- orden de pago: número, ejercicio y origen RAFAM;
- ubicación: oficina, responsable, fecha de entrega y fecha de devolución.

## Reglas de calidad

1. Catálogos para secretarías, dependencias, proveedores, tipos de servicio, frecuencias, estados y motivos.
2. Campos obligatorios validados antes de guardar.
3. No borrar físicamente datos maestros: se desactivan y se conserva el motivo.
4. Todo archivo recibido se conserva con fecha, origen y checksum.
5. Los cambios relevantes registran usuario, fecha, valor anterior y valor nuevo.
6. Las importaciones de Excel pasan por una vista de errores antes de confirmar.
7. Los contratos activos generan períodos esperados para conciliación.
8. La factura no se considera correctamente validada hasta que su boca, cuenta, período e imputación estén controlados.
9. Una liquidación no se considera completa hasta que esté vinculada a un expediente y alcance.
10. Una orden de pago RAFAM es una referencia adicional y nunca reemplaza el vínculo factura-pago.
11. Los expedientes físicos tienen historial de ubicación y responsable.

## Evolución

1. MVP: ABM de catálogos, domicilios, dependencias y bocas de servicio.
2. Contratos, cuentas y calendario esperado de facturación.
3. Importación validada desde Excel y conciliación de faltantes/novedades.
4. Liquidaciones, expedientes, alcances, órdenes RAFAM y ubicación física.
5. Facturas, imputaciones, pagos, documentos y auditoría.
6. Reportes de gasto e integración con sistemas institucionales.
7. IA asistida para análisis, alertas y explicación de variaciones.
