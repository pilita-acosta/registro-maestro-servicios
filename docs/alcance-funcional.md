# Alcance funcional

## Entidades principales

| Entidad | Responsabilidad |
| --- | --- |
| PuntoServicio | Lugar físico o dependencia donde se presta un servicio. Tiene identificador interno estable. |
| Dependencia | Hospital, CAPS, oficina u otra unidad municipal. |
| Secretaria | Área administrativa a la que se asigna una dependencia o gasto. |
| Proveedor | Empresa que presta y factura el servicio. |
| Servicio | Agua, luz, gas, internet u otro tipo catalogado. |
| Cuenta | Relación entre punto, proveedor y servicio; contiene NIS, número de cuenta o código externo. |
| Factura | Documento de un período, con importe, vencimiento, estado y archivo original. |
| Pago | Aplicación de un pago a una factura, con fecha, importe, comprobante e imputación. |
| RegistroDocumentacion | Recepción de un conjunto documental y sus datos de origen. |
| MovimientoDocumentacion | Historial de circulación entre oficinas y responsables. |
| Importacion | Lote recibido desde un proveedor, con archivo original, perfil aplicado, errores y resultado. |

## ABM y reglas

Cada ABM debe permitir alta, consulta, modificación y baja lógica. Los campos de catálogo se seleccionan, no se escriben libremente. Las asignaciones a secretaría y los cambios de proveedor o cuenta deben conservar fecha de inicio, fecha de fin, usuario y motivo.

No se debe borrar una factura, pago, documento o importación confirmada. Si hay un error, se corrige mediante una operación auditada.

## Importación masiva

El flujo será:

1. Registrar el archivo original y su origen.
2. Seleccionar o crear un perfil de proveedor.
3. Mapear columnas externas a campos internos.
4. Normalizar fechas, importes, identificadores y nombres.
5. Detectar duplicados, cuentas desconocidas, períodos repetidos y campos obligatorios faltantes.
6. Mostrar una previsualización con errores y advertencias.
7. Confirmar solo las filas válidas o corregidas.
8. Guardar el resultado del lote y el historial de cambios.

## Estados de factura

`recibida` -> `validada` -> `en_proceso` -> `pagada`.

También puede pasar a `observada`, `rechazada`, `anulada` o `pago_parcial`. El estado no reemplaza al historial de pagos.

## Dashboard inicial

Indicadores: gasto total y pagado por período, deuda pendiente, facturas vencidas, cantidad de facturas por estado, gasto por servicio/proveedor/secretaría y variación mensual. Cada indicador debe permitir llegar al listado de facturas que lo compone.
