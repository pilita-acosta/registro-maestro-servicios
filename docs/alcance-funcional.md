# Alcance funcional

## Entidades principales

| Entidad | Responsabilidad |
| --- | --- |
| Dependencia | Unidad organizativa del organigrama municipal: hospital, CAPS, oficina, dirección o área. Pertenece a una Secretaría vigente y puede funcionar en uno o más domicilios a lo largo del tiempo. |
| Domicilio | Ubicación física normalizada. Un domicilio puede alojar muchas dependencias de distintas secretarías y muchos puntos de servicio. |
| PuntoServicio | Inmueble, sede o boca operativa que identifica un servicio concreto en un domicilio. En esta etapa, todos los inmuebles alquilados gestionados por Servicios pueden registrarse como puntos de servicio, aunque todavía no tengan una cuenta o factura asociada. No es sinónimo de factura ni de proveedor. |
| Secretaria | Área del organigrama municipal que contiene dependencias y puede recibir la imputación de un gasto. |
| PersonaEntidad | Persona física, jurídica u organismo que puede intervenir en el circuito con uno o más roles. |
| Proveedor | Empresa u organismo que presta y/o factura el servicio. No incluye automáticamente al propietario ni al destinatario del pago. |
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
| InmuebleAlquilado | Inmueble ocupado por la Municipalidad mediante un alquiler, con propietario, contrato de alquiler, vigencia y expediente propio. |
| DestinatarioPago | Persona o entidad a la que efectivamente se paga: proveedor del servicio, propietario o tercero autorizado. Una compensación no es una persona, sino una modalidad de resolución. |
| ModalidadLiquidacion | Forma administrativa de resolver el gasto: pago directo, reintegro a mes vencido, pago al propietario o compensación con el proveedor. |
| LineaTelefonica | Servicio o número telefónico contratado con un proveedor, con plan, estado, usuario o destino y vigencia. |
| DispositivoMovil | Equipo celular asociado a una línea, identificado por IMEI y sujeto al control de bienes inventariables. |
| NotaPedido | Solicitud administrativa de compra de dispositivos o contratación relacionada con telefonía móvil. |
| IncidenciaTelefonia | Reclamo, corte, error de facturación, bloqueo o conflicto con el proveedor de una línea o dispositivo. |
| RegistroPatrimonial | Referencia al alta, asignación, transferencia, baja o estado patrimonial de un dispositivo. |

## ABM y reglas

Cada ABM debe permitir alta, consulta, modificación y baja lógica. Los campos de catálogo se seleccionan, no se escriben libremente. Las asignaciones de una dependencia a una secretaría, de una dependencia a un domicilio y los cambios de proveedor, contrato o cuenta deben conservar fecha de inicio, fecha de fin, usuario y motivo.

### Jerarquía y ocupación física

La jerarquía administrativa y la ubicación física son dimensiones distintas:

```text
Secretaría
  └── Dependencia
	  └── ocupación histórica de uno o más Domicilios
		  └── PuntosServicio y Cuentas de los servicios contratados
```

Un domicilio no pertenece a una única secretaría. Por ejemplo, Dardo Rocha o Torre 1 pueden alojar oficinas de varias secretarías; la República de los Niños puede tener una dependencia de una sola secretaría y, aun así, muchos servicios, cuentas y proveedores. El sistema debe mostrar ambas vistas: el organigrama y la composición del domicilio.

La relación `Dependencia-Domicilio` debe tener vigencia, fecha de inicio, fecha de fin, motivo y responsable. Una mudanza cierra la ocupación anterior y crea una nueva, sin borrar la historia. Una dependencia puede tener más de un domicilio vigente si realmente funciona en sedes simultáneas.

El ABM debe estar separado por responsabilidad: catálogos, domicilios y dependencias, puntos/bocas de servicio, contratos y cuentas, facturas, pagos, imputaciones e importaciones. No se debe permitir crear una factura sin poder identificar su proveedor, servicio, cuenta externa y período.

### Prioridad del MVP: liquidación y control de facturas

El objetivo principal del MVP es asegurar que las facturas de servicios de los inmuebles alquilados lleguen, se controlen y se liquiden a tiempo para evitar demoras, reclamos tardíos y cortes de servicio. El padrón de puntos, domicilios, dependencias y proveedores existe para hacer posible esa liquidación, no como un fin independiente.

Todos los inmuebles alquilados gestionados por el área de Servicios se pueden registrar como puntos de servicio. El campo `uso` describe qué funciona en ese inmueble o para qué se utiliza, pero no reemplaza la dependencia, la secretaría, la cuenta ni el servicio.

La modalidad preferida para resolver el gasto es el reintegro a mes vencido, siempre que el propietario o responsable entregue la documentación necesaria. Las facturas de alquileres antiguos que formen parte de convenios o resúmenes de ABSA, EDELAP, Camuzzi u otro proveedor pueden resolverse mediante compensación. Cuando una factura no entre en compensación, debe existir un circuito para que la persona responsable del inmueble la entregue dentro del plazo.

El sistema debe controlar la fecha esperada de recepción y emitir una alerta antes del vencimiento o del plazo operativo de pago. Si la factura no llega, debe avisar al responsable y permitir registrar el reclamo al propietario, a la dependencia usuaria o al proveedor. La falta de entrega no debe quedar como un problema informal: debe ser visible, trazable y escalable hasta su resolución.

La liquidación debe separar siempre estas etapas: factura esperada, factura recibida, factura controlada, factura aprobada para liquidar, modalidad de resolución elegida, imputación, documentación enviada a Contaduría y pago o compensación confirmado. Una factura recibida no equivale a una factura controlada ni pagada.

### Inmuebles alquilados y destinatario del pago

Los inmuebles alquilados forman parte del padrón de domicilios, pero no deben confundirse con dependencias ni con propietarios. Un mismo inmueble puede alojar una o varias dependencias y tener muchos servicios. El propietario activo se registra como persona o entidad vinculada al contrato de alquiler; no se reemplaza el proveedor real del servicio.

Los servicios de un inmueble alquilado pueden resolverse de distintas maneras:

- pago directo a la empresa proveedora del servicio;
- reintegro a mes vencido al propietario, contra documentación presentada;
- tratamiento del propietario como destinatario o proveedor administrativo de la Municipalidad, aunque la factura original corresponda a la empresa de servicios;
- compensación con el proveedor, cuando el proveedor envía un resumen o crédito que se imputa contra obligaciones de la Municipalidad.

La modalidad puede variar por inmueble, servicio, período o contrato. El sistema debe conservar el proveedor real, el titular o presentante de la factura, el destinatario del pago y el vínculo con el contrato de alquiler. Nunca debe asumir que quien recibe el pago es quien prestó el servicio.

Los inmuebles alquilados generan expedientes separados de los expedientes de contratación o facturación de servicios. El sistema guarda las referencias y relaciones necesarias para navegar entre inmueble, alquiler, servicio, factura, expediente, liquidación y pago, sin reemplazar el sistema institucional de expedientes.

La compensación es un paso administrativo posterior a la validación: primero se controla que el resumen del proveedor, sus facturas o sus conceptos sean correctos; luego se registra qué importe se compensa, contra qué obligación, con qué período y qué saldo queda. La compensación no elimina la factura ni evita el control de facturación.

### Telefonía celular y dispositivos

La gestión de celulares es un módulo relacionado, pero distinto del padrón de servicios del domicilio. Una línea y un dispositivo no son la misma cosa: una línea puede cambiar de equipo y un equipo puede quedar sin línea, ser reasignado o darse de baja. El IMEI identifica al dispositivo y el número telefónico identifica la línea; ninguno debe ser el identificador interno principal.

El circuito contempla nota de pedido, expediente iniciado a partir de esa nota, recepción y entrega de equipos, coordinación con Patrimonio por tratarse de bienes inventariables, y registro de marca, modelo, IMEI, estado y referencia patrimonial. También contempla incidencias de línea o equipo, reclamos y conflictos con el proveedor, con solución, responsable, fecha, número de reclamo y documentación respaldatoria.

El sistema no reemplaza el alta ni los movimientos oficiales de Patrimonio. Una incidencia no se cierra solo porque el proveedor respondió: debe verificarse la solución y conservarse el historial.

### Regla de identidad de una boca

El domicilio no identifica por sí solo un punto de servicio. La identidad operativa se compone de:

`dependencia + domicilio vigente + tipo de servicio + proveedor + cuenta externa + vigencia`

Por ejemplo, el mismo domicilio puede tener dos cuentas de internet con proveedores distintos, o dos suministros del mismo proveedor. Cada relación debe tener su propio identificador interno y conservar sus códigos externos.

La combinación se valida para detectar duplicados, pero no se usa como clave primaria. La cuenta externa identifica la relación del proveedor con el servicio y debe conservarse aunque la oficina se mude o cambie la secretaría responsable. Si cambia el medidor, suministro o identificador externo, se cierra la cuenta anterior y se registra una nueva.

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

Los estados representan etapas distintas y no deben mezclarse:

`recibida` -> `observada` o `validada` -> `aprobada_para_liquidar` -> `en_liquidacion` -> `enviada_a_contaduria` -> `pagada`.

También puede pasar a `rechazada`, `anulada` o `pago_parcial`. El estado no reemplaza al historial de pagos. Una factura puede estar validada y todavía impaga; el pago no debe inferirse por el estado de la liquidación.

### Identidad y duplicados de facturas

La identidad principal de una factura es `proveedor + número de factura`. El número debe conservarse en formato original y normalizado. Si el proveedor no entrega un número confiable, la factura no se duplica automáticamente: queda observada y se intenta detectar coincidencia por cuenta, período e importe como regla secundaria.

### Cambios de proveedor

Un cambio de proveedor significa que el mismo punto físico o dependencia comienza a recibir el servicio de otra empresa. No se modifica el proveedor de las facturas históricas. Se cierra la vigencia del contrato o relación anterior y se crea una nueva relación para el proveedor entrante. La cuenta externa solo se reemplaza si el proveedor asigna otro identificador; si conserva el mismo número, se mantiene ese dato y se registra el cambio de proveedor con su vigencia y motivo.

## Imputación y dashboard inicial

Luego de validar una importación, cada factura debe asociarse a una boca y obtener su secretaría responsable desde la asignación vigente. Si el gasto corresponde a más de una secretaría, se registra una imputación múltiple sin romper la relación factura-pago.

La liquidación agrupa las facturas que se tramitan juntas, se vincula al contrato y al alcance de expediente correspondiente, y luego registra la orden de pago RAFAM. Esta agrupación no debe mover ni copiar facturas: solo establece una relación consultable. En una liquidación global, la relación incluye muchas cuentas, domicilios y secretarías.

La suma de imputaciones de una factura debe coincidir con el importe facturado, salvo que quede una diferencia explícita en estado observado. Contaduría debe poder obtener un resumen por secretaría, período, servicio y proveedor, y navegar desde ese total hasta las facturas y pagos que lo componen.

Indicadores: gasto facturado y pagado por período, deuda pendiente, facturas vencidas, facturas faltantes, bocas nuevas, contratos sin facturación, cantidad por estado, gasto por servicio/proveedor/secretaría y variación mensual. Cada indicador debe permitir llegar al listado de registros que lo compone.

## Control de datos

Las validaciones se ejecutan en cinco momentos: al importar, al asociar una factura a una boca, al confirmar la imputación, antes de cerrar una liquidación y antes de asociar una orden de pago. Toda excepción requiere motivo y responsable. El sistema debe conservar el archivo original, la fila de origen, el valor normalizado y el resultado de la validación.

Antes de cerrar una liquidación se debe verificar: contrato vigente, facturas esperadas conciliadas, facturas sin duplicar, boca y cuenta identificadas, imputaciones completas, alcance correcto y, cuando exista, orden de pago RAFAM vinculada. Una baja operativa solo puede cerrarse cuando se registró la gestión de baja ante el proveedor, su fecha, comprobante o referencia y el responsable que la confirmó.

## Evolución con IA

La IA se incorpora después de contar con datos históricos confiables y reglas auditables. Su primer uso debe ser analítico y asistido: explicar variaciones, detectar consumos o importes atípicos, sugerir posibles duplicados y resumir por qué una liquidación quedó observada. No debe aprobar facturas, modificar datos maestros ni decidir imputaciones automáticamente.
