# Alcance funcional

## Entidades principales

| Entidad | Responsabilidad |
| --- | --- |
| Dependencia | Hospital, CAPS, oficina u otra unidad municipal. Es la unidad organizativa que funciona en un domicilio. |
| Domicilio | Ubicación física normalizada. Un domicilio puede alojar una o varias dependencias y muchas bocas de servicio. |
| PuntoServicio | Boca o activo físico/administrativo que identifica un servicio concreto en un domicilio. No es sinónimo de factura ni de proveedor. |
| Secretaria | Área administrativa a la que se asigna una dependencia o gasto. |
| Proveedor | Empresa que presta y factura el servicio. |
| Servicio | Agua, luz, gas, internet u otro tipo catalogado. |
| Contrato | Define proveedor, servicio, vigencia, frecuencia de facturación y reglas esperadas. |
| Cuenta | Identificación externa del proveedor para una boca: NIS, número de cuenta, medidor, suministro o código equivalente. |
| Factura | Documento de un período, con importe, vencimiento, estado, origen y archivo original. |
| Imputacion | Distribución del gasto de una factura entre una o más secretarías, con porcentajes o importes. |
| Pago | Aplicación de uno o varios pagos a una factura, con fecha, importe, comprobante e imputación. |
| RegistroDocumentacion | Recepción de un conjunto documental y sus datos de origen. |
| MovimientoDocumentacion | Historial de circulación entre oficinas y responsables. |
| Importacion | Lote recibido desde un proveedor, con archivo original, perfil aplicado, errores, advertencias y resultado. |
| Conciliacion | Resultado de comparar el universo esperado contra las facturas recibidas y aceptadas. |

## ABM y reglas

Cada ABM debe permitir alta, consulta, modificación y baja lógica. Los campos de catálogo se seleccionan, no se escriben libremente. Las asignaciones a secretaría y los cambios de proveedor, contrato o cuenta deben conservar fecha de inicio, fecha de fin, usuario y motivo.

El ABM debe estar separado por responsabilidad: catálogos, domicilios y dependencias, puntos/bocas de servicio, contratos y cuentas, facturas, pagos, imputaciones e importaciones. No se debe permitir crear una factura sin poder identificar su proveedor, servicio, cuenta externa y período.

### Regla de identidad de una boca

El domicilio no identifica por sí solo un punto de servicio. La identidad operativa se compone de:

`domicilio + dependencia + tipo de servicio + proveedor + cuenta externa + vigencia`

Por ejemplo, el mismo domicilio puede tener dos cuentas de internet con proveedores distintos, o dos suministros del mismo proveedor. Cada relación debe tener su propio identificador interno y conservar sus códigos externos.

La combinación se valida para detectar duplicados, pero no se usa como clave primaria: los datos del proveedor pueden cambiar, llegar incompletos o corregirse con el tiempo.

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
9. Ejecutar la conciliación contra el padrón de bocas y contratos esperados.

## Control de facturación y faltantes

Para cada contrato activo se calcula un calendario esperado según su frecuencia: mensual, bimestral, trimestral, cuatrimestral, semestral, anual u otra definida contractualmente. La frecuencia no se deduce únicamente de las facturas recibidas.

La conciliación debe clasificar cada contrato y período como:

- `recibida`: llegó una factura esperada.
- `faltante`: no llegó una factura dentro del período esperado.
- `no_corresponde`: el período está fuera de vigencia o existe una justificación registrada.
- `nueva_boca`: apareció una cuenta o relación no existente en el padrón.
- `observada`: llegó, pero tiene inconsistencias.
- `duplicada`: coincide con una factura ya registrada.

Una factura de una boca nueva no se incorpora silenciosamente al padrón. Se crea una alerta y queda pendiente de validación, con motivo, responsable y resolución.

## Estados de factura

`recibida` -> `validada` -> `en_proceso` -> `pagada`.

También puede pasar a `observada`, `rechazada`, `anulada` o `pago_parcial`. El estado no reemplaza al historial de pagos.

## Imputación y dashboard inicial

Luego de validar una importación, cada factura debe asociarse a una boca y obtener su secretaría responsable desde la asignación vigente. Si el gasto corresponde a más de una secretaría, se registra una imputación múltiple sin romper la relación factura-pago.

La suma de imputaciones de una factura debe coincidir con el importe facturado, salvo que quede una diferencia explícita en estado observado. Contaduría debe poder obtener un resumen por secretaría, período, servicio y proveedor, y navegar desde ese total hasta las facturas y pagos que lo componen.

Indicadores: gasto facturado y pagado por período, deuda pendiente, facturas vencidas, facturas faltantes, bocas nuevas, contratos sin facturación, cantidad por estado, gasto por servicio/proveedor/secretaría y variación mensual. Cada indicador debe permitir llegar al listado de registros que lo compone.

## Control de datos

Las validaciones se ejecutan en cuatro momentos: al importar, al asociar una factura a una boca, al confirmar la imputación y antes de cerrar una liquidación. Toda excepción requiere motivo y responsable. El sistema debe conservar el archivo original, la fila de origen, el valor normalizado y el resultado de la validación.

## Evolución con IA

La IA se incorpora después de contar con datos históricos confiables y reglas auditables. Su primer uso debe ser analítico y asistido: explicar variaciones, detectar consumos o importes atípicos, sugerir posibles duplicados y resumir por qué una liquidación quedó observada. No debe aprobar facturas, modificar datos maestros ni decidir imputaciones automáticamente.
