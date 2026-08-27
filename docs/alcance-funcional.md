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
| Expediente | Referencia al expediente único generado por el sistema institucional para un contrato. El sistema no reemplaza ni duplica el expediente. |
| Alcance | Actuación asociada a una liquidación dentro de un expediente, por ejemplo `EXP 4061-2014072/2026 - ALC 1`. |
| Liquidacion | Corte o conjunto de facturas que se prepara para tramitar y pagar en un período. Puede ser individual o global. |
| LiquidacionGlobal | Lote masivo enviado por un proveedor como ABSA, EDELAP o Camuzzi, con muchas facturas, domicilios y cuentas que se distribuyen entre varias secretarías. |
| Cuenta | Identificación externa del proveedor para una boca: NIS, número de cuenta, medidor, suministro o código equivalente. |
| Factura | Documento de un período, con importe, vencimiento, estado, origen y archivo original. |
| Imputacion | Distribución del gasto de una factura entre una o más secretarías, con porcentajes o importes. |
| Pago | Aplicación de uno o varios pagos a una factura, con fecha, importe, comprobante e imputación. |
| OrdenPago | Número generado por RAFAM, vinculado al alcance y al pago para facilitar búsquedas cruzadas. |
| UbicacionExpediente | Área, oficina o persona que tiene el expediente físico, con fecha de entrega y devolución. |
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

## Expedientes, alcances y RAFAM

El sistema será un índice de consulta y trazabilidad. Expedientes y contratos continúan siendo gestionados por sus sistemas institucionales y en soporte papel; solo se almacenan sus identificadores, vínculos y movimientos necesarios para localizar la información.

- Un `Contrato` puede tener un único expediente principal externo.
- Cada `Liquidacion` se vincula a un `Alcance` del expediente.
- Cada alcance conserva número, año, fecha, período liquidado, importe y estado.
- Una orden de pago RAFAM se vincula al alcance, pero no reemplaza la relación con factura, imputación o pago.
- Un expediente puede tener múltiples alcances, y cada alcance puede contener muchas facturas.
- La ubicación física registra quién tiene el expediente, desde cuándo, dónde debe devolverse y cuándo fue devuelto.

### Liquidaciones globales

Proveedores como ABSA, EDELAP y Camuzzi pueden enviar una facturación global. El archivo o lote recibido se considera una unidad de origen, pero cada fila o factura debe poder rastrearse individualmente:

```text
Liquidación global del proveedor
	↓
Facturas / filas de origen
	↓
Cuenta externa y PuntoServicio
	↓
Domicilio y Dependencia
	↓
Secretaría vigente
	↓
Imputación individual
	↓
Resumen agrupado por Secretaría
```

La liquidación global debe conservar el total informado por el proveedor, la cantidad de registros recibidos y el archivo original. El sistema debe calcular el total validado, el total observado, el total imputado y las diferencias.

El resumen para Contaduría se genera después de validar cada factura, no antes. Una misma liquidación global puede producir una lista de muchas secretarías con sus montos asignados, manteniendo el detalle que explica cada total.

La pantalla debe permitir navegar desde la global hacia sus facturas, cuentas, domicilios y secretarías, y también desde una secretaría o factura hacia la global, expediente, alcance y orden de pago relacionados.

Ejemplo de referencia:

```text
Contrato: CT-2026-014
Expediente: 4061-2014072/2026
Liquidación: junio 2026
Alcance: 1
Orden de pago RAFAM: OP-00012345
Facturas: F-001, F-002, F-003
Imputación: Secretaría de Salud
Estado: enviado a Contaduría
Ubicación física: Contaduría · responsable registrado
```

El número de expediente, alcance y orden de pago se guardan como referencias normalizadas y también con el texto original recibido, para no perder la forma en que se encuentra en el papel o sistema externo.

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
10. Generar o asociar una liquidación y su alcance de expediente.
11. Registrar la orden de pago RAFAM cuando sea creada.

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

La liquidación agrupa las facturas que se tramitan juntas, se vincula al contrato y al alcance de expediente correspondiente, y luego registra la orden de pago RAFAM. Esta agrupación no debe mover ni copiar facturas: solo establece una relación consultable. En una liquidación global, la relación incluye muchas cuentas, domicilios y secretarías.

La suma de imputaciones de una factura debe coincidir con el importe facturado, salvo que quede una diferencia explícita en estado observado. Contaduría debe poder obtener un resumen por secretaría, período, servicio y proveedor, y navegar desde ese total hasta las facturas y pagos que lo componen.

Indicadores: gasto facturado y pagado por período, deuda pendiente, facturas vencidas, facturas faltantes, bocas nuevas, contratos sin facturación, cantidad por estado, gasto por servicio/proveedor/secretaría y variación mensual. Cada indicador debe permitir llegar al listado de registros que lo compone.

## Control de datos

Las validaciones se ejecutan en cinco momentos: al importar, al asociar una factura a una boca, al confirmar la imputación, antes de cerrar una liquidación y antes de asociar una orden de pago. Toda excepción requiere motivo y responsable. El sistema debe conservar el archivo original, la fila de origen, el valor normalizado y el resultado de la validación.

Antes de cerrar una liquidación se debe verificar: contrato vigente, facturas esperadas conciliadas, facturas sin duplicar, boca y cuenta identificadas, imputaciones completas, alcance correcto y, cuando exista, orden de pago RAFAM vinculada.

## Evolución con IA

La IA se incorpora después de contar con datos históricos confiables y reglas auditables. Su primer uso debe ser analítico y asistido: explicar variaciones, detectar consumos o importes atípicos, sugerir posibles duplicados y resumir por qué una liquidación quedó observada. No debe aprobar facturas, modificar datos maestros ni decidir imputaciones automáticamente.
