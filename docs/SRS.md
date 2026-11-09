# Introducción[^c0]

El presente documento constituye la Especificación de Requisitos de Software (SRS) para el Sistema de Gestión de Minimercado de la Cigarrería Alcalá. En él se describen el propósito y el alcance del sistema a desarrollar, las definiciones y términos empleados a lo largo del documento, las referencias utilizadas para su elaboración, y un resumen de la organización del contenido, como base para la definición posterior de los requisitos funcionales y no funcionales del sistema.

## Propósito[^c1]

1.1 Objetivo General: Definir los requisitos funcionales y no funcionales para el desarrollo del sistema de gestión de inventario, compras y ventas de la Cigarrería Alcalá.

1.2 Objetivos Específicos:

		- Registrar formalmente las entradas de mercancía basadas en facturas de proveedores y las salidas por ventas en el mostrador, para mantener actualizado en todo momento el stock disponible.

		- Centralizar la información tributaria (RUT) y de contacto de las 50 empresas distribuidoras, permitiendo el seguimiento del ciclo de compras desde la toma del pedido hasta la entrega.

		- Proporcionar un mecanismo que permita registrar y comparar la cantidad facturada por el proveedor con la cantidad efectivamente recibida por la encargada del local, con el fin de identificar y documentar discrepancias en el inventario.

		- Configurar un sistema de alertas visuales para niveles mínimos de existencias (respetando el cupo máximo de 30 unidades por producto) y aplicar el criterio de salida FIFO (First In, First Out), priorizando siempre la salida del lote más antiguo de cada producto.

Este documento está dirigido principalmente al equipo de desarrollo encargado de construir el sistema, como base para el diseño y la implementación de las funcionalidades descritas. Así mismo, está dirigido a la dueña de la Cigarrería Alcalá, como usuaria y cliente final, para validar que los requisitos documentados reflejan correctamente sus necesidades operativas. Adicionalmente, sirve como material de evaluación para el docente de la asignatura de Bases de Datos.

## Alcance[^c2]

El producto a desarrollar es el Sistema de Gestión para la Cigarrería Alcalá, una aplicación web orientada al control de productos, proveedores, pedidos, inventario y ventas del minimercado. Este proyecto no cuenta con documentos de mayor nivel previos, por lo que el alcance aquí definido es consistente únicamente con la narrativa del proceso de negocio levantada directamente con la dueña del establecimiento.

Estado actual de la empresa

La Cigarrería Alcalá comercializa una amplia variedad de mercancías para el consumo diario: bebidas, abarrotes, snacks y algunos productos de primera necesidad, situándose en el área de aplicación comercial. Trabaja con cerca de 50 empresas proveedoras.

Actualmente, el establecimiento no lleva un inventario formal: no existe un registro de existencias, solo de lo que le llega. Tampoco anota la mercancía vendida: no se emite ningún comprobante ni se lleva un registro de la transacción. La encargada del local lleva un registro manual independiente de la mercancía que efectivamente recibe, el cual no siempre coincide en los detalles con la factura del proveedor. La alerta de stock mínimo es solo visual.

Cuenta con un celular y red de Wi-Fi, y con un presupuesto de 1 800 000 de pesos colombianos.

**Identidad empresarial**

La identidad cromática de la Cigarrería Alcalá se compone de rojo como color primario, que transmite energía y apetito y refuerza la conexión visual ya establecida con la marca Postobón que identifica el local; amarillo/naranja como color secundario, que evoca cercanía, calidez y accesibilidad, características de una tienda de barrio; y blanco/gris claro como color neutro, que aporta orden y limpieza visual, en línea con la buena presentación e higiene que debe proyectar un establecimiento de venta de alimentos y bebidas.

En cuanto a tipografía, los encabezados y el nombre de la marca usan una tipografía redondeada y amigable, que refuerza la cercanía de una tienda de barrio, mientras que el cuerpo de texto y los datos numéricos (precios, cantidades, tablas de inventario) usan una tipografía de alta legibilidad, que facilita la lectura rápida de cifras durante la atención al cliente.

Procesos

1. Proceso de registro de productos

Cada producto que se ofrece se identifica mediante un código, un nombre comercial, una categoría (bebida, snack/abarrote, lácteo) con una descripción, una presentación (botella retornable, plástico desechable, lata, bolsa o caja), un precio de compra al proveedor y un precio de venta al público. Para la gestión de precios, ella ve cuántas unidades vienen en la caja, divide el precio de la caja entre esa cantidad para sacar el valor unitario y a ese valor le suma un 20 o 25% para las utilidades.

2. Proceso de recepción de pedidos a proveedores

La cigarrería trabaja con empresas proveedoras, cada una identificada por su RUT, razón social y teléfono de contacto. Cada proveedor envía a uno o varios vendedores que visitan diariamente el local para tomar el pedido; de cada vendedor se registra su nombre y su número de contacto.

Cuando el vendedor visita el local, cotiza cada producto solicitado indicando su precio por unidad, y con esa información se registra en el pedido hecho antes de la cotización: la fecha de solicitud, la fecha estimada de entrega y el detalle de lo cotizado (producto, cantidad, precio por unidad y precio acordado en ese momento).

Días después, al llegar la mercancía, el proveedor emite la factura de compra correspondiente, la cual incluye un código, la fecha de emisión, la fecha de recepción y el detalle de los productos entregados con su respectivo código, nombre, cantidades y precios pactados. Cada entrega recibida se convierte en un lote independiente de mercancía, del cual se registra la cantidad recibida y la fecha de vencimiento.

Por su parte, la encargada del local lleva un registro manual independiente de la mercancía que efectivamente recibe, el cual no siempre coincide en los detalles con la factura del proveedor, ya sea por un producto faltante, uno distinto, o de un producto con un sabor diferente al pedido.

3. Proceso de inventario

Para cada producto se debe conocer en todo momento cuántas unidades hay disponibles en el local (el stock actual), así como un umbral mínimo de existencias que, al alcanzarse, debe generar una alerta.

4. Proceso de registro de ventas

El sistema debe generar por cada venta un registro interno con la fecha y el monto total pagado, junto con el detalle de qué productos, su código, precio unitario y en qué cantidad salieron del local en esa transacción; información que también debe reflejarse en la disponibilidad de cada producto y en la salida del lote correspondiente.

Reglas del negocio

- Productos y precios

		- De cada producto se manejan un máximo de 30 unidades disponibles simultáneamente en el local, debido a las limitaciones de espacio. Este máximo aplica al producto en general y no a cada lote por separado; no es necesario que la suma sea exactamente 30, las unidades sobrantes simplemente se mantienen.

		- Cuando el producto ya viene con precio sugerido, normalmente se respeta; solo cuando el precio no está escrito en el empaque, se le agrega un 20%.

		- Cuando un producto no viene en caja se vende suelto, y el precio depende de cómo se compró (lo más común es que llegue en caja o empacado con varias unidades).

		- Presentaciones distintas de un mismo producto (por ejemplo, una gaseosa en botella y en lata) se manejan como productos separados; cuando cambia el gramaje de un producto, el precio se ajusta hacia arriba o hacia abajo según corresponda.

		- Todos los productos manejan fecha de vencimiento, no solo los lácteos.

- Proveedores y pedidos

		- Los vendedores van a buscar los clientes; la selección depende de los precios que maneje el vendedor: si son rentables se aceptan, si no se descartan.

		- Un mismo proveedor puede ofrecer el mismo producto a precios distintos según el vendedor que visite ese día; por lo general se intenta quedarse con el precio más bajo, pero si el producto es de primera necesidad, el precio deja de ser un criterio decisivo.

		- Para efectos del sistema no se registran los datos del vendedor: el teléfono del proveedor es suficiente como dato de contacto para reclamos.

		- Una vez cotizado, el pedido no se puede cancelar ni modificar, porque queda pactado y la factura se genera con esa información.

		- Si el pedido no llega en la fecha estimada, el sistema debe avisar o marcarlo como atrasado.

		- Los precios pactados en la factura de compra pueden variar respecto al precio de compra habitual del producto.

- Recepción y lotes

		- Cada entrega recibida se convierte en un lote independiente.

		- Un producto está próximo a vencer cuando faltan máximo 5 días para su vencimiento. En ese caso se puede comercializar a un precio inferior al recomendado; este descuento se decide caso por caso, ocurre rara vez, y cuando ocurre se vende al precio de compra para no perder lo invertido.

		- Si un producto ya venció, se desecha, y se debe registrar cuánto dinero se perdió en la mercancía vencida.

		- Cuando hay una discrepancia entre la factura y lo recibido, queda registrada como una nota. Si se decide quedarse con un producto distinto al pedido, ese producto entra al sistema como uno nuevo, no como el que originalmente se pidió.

		- La constancia de cualquier reclamo al proveedor es la propia factura de los productos entregados; no se guarda ninguna otra evidencia adicional.

		- Si un pedido entrante haría que un producto supere el límite de 30 unidades, el sistema debe avisar antes de aceptar la entrega completa.

- Inventario

		- El umbral mínimo de existencias es el mismo número para todos los productos; no varía según qué tan rápido se venda cada uno.

		- Con que la alerta se vea al abrir la aplicación es suficiente; no se necesita notificación push al celular.

- Ventas

		- El precio de venta es el que está registrado; no se manejan descuentos ni promociones en el mostrador (como 2x1 o combos), salvo la rebaja excepcional por producto próximo a vencer.

		- La salida de mercancía prioriza siempre el lote más antiguo.

		- Algunos clientes fieles tienen crédito (fiado) y normalmente pagan dentro de los 5 días siguientes.

		- Las devoluciones de clientes no vuelven al stock: se desechan o se le devuelven al proveedor.

		- La mayoría de los pagos son en efectivo, pero también se aceptan transferencias o Nequi/Daviplata, aunque rara vez y solo para compras superiores a $10.000. El sistema debe diferenciar el medio de pago usado en cada venta.

Propuesta de solución

El sistema se usaría diariamente en la tienda, en tres momentos por igual: al recibir mercancía, al vender y para consultar qué le queda. Como el negocio cuenta solo con un celular y red Wi-Fi, necesita que el sistema funcione sin conexión a internet al menos por un rato.

El aplicativo incluirá:

		- Un módulo para el control de acceso al sistema mediante un inicio de sesión para la dueña del negocio.

		- Un módulo para un menú estructurado que permita el desplazamiento fluido entre los diferentes formularios del sistema.

		- Un módulo para el registro y actualización de los datos de los productos (código, nombre comercial, categoría, presentación, precio de compra y precio de venta).

		- Un módulo para el registro y gestión de las 50 empresas proveedoras (RUT, razón social y teléfono) y sus pedidos.

		- Un módulo para el registro de las cotizaciones acordadas por pedido y de las facturas de compra recibidas.

		- Un módulo para el registro de la mercancía recibida en lotes independientes por cada entrega, incluyendo cantidad y fecha de vencimiento.

		- Un módulo para la consulta en todo momento del stock disponible por producto y la generación de alertas visuales al alcanzar el umbral mínimo de existencias.

		- Un módulo para el registro de las ventas mediante una factura interna, descontando automáticamente la mercancía del lote más antiguo disponible.

		- Un módulo para el registro de pérdidas por mercancía vencida y desechada.

		- Un módulo para la generación de reportes de ventas del día, productos más vendidos, ganancia del mes y productos próximos a vencer.

El aplicativo no incluirá:

		- Exportar los reportes o datos directamente a formatos Excel o PDF en esta fase.

		- Integración automática con plataformas de pago externas (Nequi, Daviplata, PSE); estos pagos se registrarán de forma manual.

		- Emisión de facturas electrónicas válidas ante la DIAN.

		- Gestión de la contabilidad tributaria formal del negocio ni de la nómina o personal de la tienda.

		- Registro o administración de clientes en general; solo se registrará el crédito puntual otorgado a clientes frecuentes.

## Personal involucrado[^c3]

| Nombre | Christopher Anthony Julca Marin |
| --- | --- |
| Rol | Arquitecto de software |
| Categoría profesional | Ingeniero de sistemas |
| Responsabilidades | Diseñar y modelar la base de datos |
| Información de contacto | +51 942108270 |
| Aprobación | [Aprobado] |

| Nombre | Juan Pablo Forero Botía |
| --- | --- |
| Rol | Diseñador de software |
| Categoría profesional | Ingeniero de sistemas |
| Responsabilidades | Especificar los requisitos del software |
| Información de contacto | +53 3228423758 |
| Aprobación | [Aprobado] |

| Nombre | Luz Marina Botia Guerrero |
| --- | --- |
| Rol | Cliente |
| Categoría profesional | Universitaria, licenciada en Educación preescolar |
| Responsabilidades | Administrar el negocio |
| Información de contacto | +53 3114607060 |
| Aprobación | [Inserte aquí el texto] |

## Definiciones, acrónimos y abreviaturas[^c4]

**Términos técnicos:**

Acrónimos:

| Término | Definición |
| --- | --- |
| SRS | Software Requirements Specification. Documento que especifica los requisitos funcionales y no funcionales de un sistema; corresponde al presente informe. |
| MER | Modelo Entidad-Relación. Representación gráfica de las entidades del sistema, sus atributos y las relaciones entre ellas. |
| FIFO | First In, First Out. Método de gestión de inventario en el que primero sale la mercancía que primero ingresó. |
| PK (Clave primaria) | Atributo o conjunto de atributos que identifica de forma única cada registro de una tabla. |
| FK (Clave foránea) | Atributo de una tabla que hace referencia a la clave primaria de otra tabla, para establecer una relación entre ambas. |

Definiciones:

| Término | Definición |
| --- | --- |
| Modelo relacional | Modelo de datos basado en tablas (relaciones), propuesto por Edgar F. Codd, en el que la información se organiza en filas y columnas. |
| Cardinalidad | Número de instancias de una entidad que pueden asociarse con instancias de otra entidad en una relación (ej. 1:N, N:M). |
| Normalización | Proceso mediante el cual se organizan los atributos y tablas de una base de datos para reducir la redundancia y evitar anomalías de actualización. |
| Forma Normal (1FN, 2FN, 3FN) | Conjunto de reglas que debe cumplir una tabla para considerarse normalizada en determinado nivel. |
| Dependencia funcional | Relación en la que el valor de un atributo determina el valor de otro atributo dentro de la misma tabla. |
| Dependencia transitiva | Dependencia funcional indirecta, en la que un atributo depende de otro que a su vez depende de la clave primaria, y no directamente de esta. |
| Atributo multivaluado / grupo repetitivo | Atributo que puede tomar varios valores para un mismo registro (ej. varios productos dentro de un mismo pedido). |
| Redundancia | Repetición innecesaria de un mismo dato en distintos lugares de la base de datos. |
| Requisito funcional | Descripción de una función o comportamiento específico que el sistema debe realizar. |
| Requisito no funcional | Condición o restricción bajo la cual debe operar el sistema (rendimiento, disponibilidad, usabilidad, etc.), sin describir una función específica. |

**Términos del contexto del negocio:**

Acrónimos:

| Término | Definición |
| --- | --- |
| RUT | Registro Único Tributario. Número que identifica formalmente a cada empresa proveedora. |

Definiciones:

| Término | Definición |
| --- | --- |
| Cigarrería Alcalá | Nombre del minimercado sobre el cual se desarrolla el sistema. |
| Proveedor | Empresa que suministra la mercancía que se comercializa en el local. |
| Pedido | Solicitud de mercancía hecha a un proveedor, con la cotización de productos, cantidades y precios acordados. |
| Factura de compra | Documento que emite el proveedor al momento de entregar la mercancía solicitada, con el detalle de los productos, cantidades y precios pactados. |
| Factura de venta | Comprobante interno generado por el sistema en cada venta realizada en el mostrador. |
| Lote | Conjunto de unidades de un mismo producto recibidas en una misma entrega, identificado de forma independiente y con su propia fecha de vencimiento. |
| Stock / Inventario | Cantidad de unidades disponibles de un producto en el local en un momento determinado. |
| Umbral mínimo | Cantidad mínima de existencias de un producto a partir de la cual el sistema debe generar una alerta de reabastecimiento. |
| Merma | Pérdida de mercancía, en este caso por vencimiento del producto, que debe desecharse. |
| Trazabilidad | Capacidad de seguir el recorrido de un producto o lote desde su recepción hasta su salida (venta o merma). |
| Celular | Dispositivo móvil desde el cual la dueña del negocio operará el sistema. |
| Wi-Fi | Red inalámbrica de conexión a internet disponible en el local, usada para el funcionamiento del sistema. |

## Referencias[^c5]

| **Referencia** | **Titulo** | **Ruta** | **Fecha** | **Autor** |
| --- | --- | --- | --- | --- |
| 1 | Especificación de Requisitos Software según el estándar de IEEE 830 | [https://textos.pucp.edu.pe/pdf/3134.pdf](https://textos.pucp.edu.pe/pdf/3134.pdf) | 24/09//2026 | Raúl Monferrer Agut |
| 2 | Guía sobre requisitos no funcionales y de proyecto | [https://cosmic-sizing.org/wp-content/uploads/2020/03/10-NFR-Guia-v1.03.pdf](https://cosmic-sizing.org/wp-content/uploads/2020/03/10-NFR-Guia-v1.03.pdf) | 24/09/2026 | COSMIC |
| 3 | Bases de datos | [https://gc.scalahed.com/recursos/files/r161r/w24819w/L1IS106/PF_L1IS106_S3.pdf](https://gc.scalahed.com/recursos/files/r161r/w24819w/L1IS106/PF_L1IS106_S3.pdf) | 24/09/2026 | UTEL Universidad |
| 4 | ¿Qué es el RUT y para qué sirve? Todo lo que necesitas saber | [https://www.siigo.com/blog/obligaciones-fiscales/que-es-el-rut-y-para-que-sirve/](https://www.siigo.com/blog/obligaciones-fiscales/que-es-el-rut-y-para-que-sirve/) | 24/09/2026 | SIIGO |
| 5 | Trazabilidad: qué es y cómo implementarla con éxito | [https://www.mecalux.com.co/blog/trazabilidad](https://www.mecalux.com.co/blog/trazabilidad) | 24/09/2026 | MECALUX |

## Resumen[^c6]

El resto del documento se organiza de la siguiente manera:

La sección 2 presenta una visión global del sistema: sus principales funciones, las características de la usuaria que lo operará, las restricciones bajo las cuales debe operar y los supuestos y dependencias que se tuvieron en cuenta durante su especificación.

La sección 3 detalla los requisitos de interfaz, los requisitos funcionales del sistema; organizados según los procesos de registro de productos, gestión de proveedores y pedidos, control de inventario y registro de ventas descritos en la introducción; y los requisitos no funcionales relacionados con usabilidad, disponibilidad y funcionamiento del sistema sin conexión a internet.

La sección 4 incluye el diagrama de contexto del sistema, la justificación de la metodología de desarrollo empleada, un prototipo de la interfaz y los anexos con los recursos de recolección de información (narrativa y entrevista) utilizados para elaborar el presente documento.

# Descripción general

## Perspectiva del producto[^c7]

Es un producto independiente. El cliente no contaba con un sistema ni con un excel que necesite migrar.

## Funcionalidad del producto[^c8]

A continuación, se relaciona un resumen de las funcionalidades principales que el producto realizará:

- El sistema permitirá controlar el acceso al sistema mediante un inicio de sesión.

- El sistema permitirá gestionar la información de los productos.

- El sistema permitirá gestionar la información de las empresas proveedoras.

- El sistema permitirá gestionar los pedidos y su factura de compra.

- El sistema permitirá controlar la mercancía recibida mediante lotes.

- El sistema permitirá consultar el stock disponible y recibir alertas cuando un producto alcance su nivel mínimo de existencias o esté próximo a vencer.

- El sistema permitirá registrar las ventas realizadasr, descontando automáticamente la mercancía más antigua disponible.

- El sistema permitirá registrar las pérdidas generadas por mercancía vencida.

- El sistema permitirá consultar reportes de ventas del día, productos más vendidos, ganancia del mes y productos próximos a vencer.

## Características de los usuarios[^c9]

| Tipo de usuario | Administrador del negocio |
| --- | --- |
| Formación | Universitaria, licenciada en Educación preescolar |
| Habilidades | Manejo de dispositivos móviles, manejo y gestión de productos |
| Actividades | Iniciar sesión en el sistema. Registrar y actualizar los productos y sus precios de compra y de venta. Registrar y gestionar los proveedores. Registrar los pedidos con las cotizaciones acordadas y hacer seguimiento a su fecha estimada de entrega. Registrar las facturas de compra y la mercancía recibida en lotes, con su cantidad y fecha de vencimiento. Anotar las discrepancias entre lo facturado y lo realmente recibido. Consultar el stock disponible y revisar las alertas de stock mínimo y de productos próximos a vencer. Registrar las ventas del mostrador mediante la factura interna. Registrar la mercancía vencida que se desecha y las pérdidas que genera. Consultar los reportes: ventas del día, productos más vendidos, ganancia del mes y productos próximos a vencer. |

## Restricciones[^c10]

A continuación, se describirá aquellas limitaciones a tener en cuenta a la hora de diseñar y desarrollar el sistema:

- El sistema debe estar en capacidad de adaptarse a un celular o computador.

- El sistema debe tener una interfaz sencilla.

- El sistema debe tener alertas, las cuales deben ser visuales y mostrarse al abrir la aplicación.

- El sistema debe permitir que cada producto tenga como máximo 30 unidades. El límite aplica al producto en general, no a cada lote, y el sistema debe avisar antes de aceptar una entrega que lo supere.

- El sistema debe hacer que el precio de venta siempre es el registrado en el sistema. No se manejan descuentos ni promociones en el mostrador. La única excepción es la venta de un producto próximo a vencer (máximo 5 días antes) al precio de compra.

- El sistema debe tener un umbral mínimo de existencias que sea un único valor para todos los productos.

- El sistema debe hacer que la salida de mercancía priorice el lote más antiguo.

- El sistema debe distinguir el medio de pago de cada venta.

- El sistema debe hacer que las devoluciones de clientes no regresen al stock.

- El sistema debe hacer que las presentaciones distintas de un mismo producto se manejen como productos separados.

- El sistema debe hacer que un producto distinto al pedido que la encargada decide conservar se registre como producto nuevo.

- El sistema debe manejar los ingresos y precios en pesos colombianos (COP).

- El sistema debe encargarse de que la información se almacene en una base de datos que conserve el historial de ventas, lotes, facturas de compra y pérdidas por vencimiento, y que solo pueda ser consultada por la encargada del local.

## Suposiciones y dependencias[^c11]

Si alguno de los siguientes factores cambia, los requisitos del sistema podrían verse afectados y la SRS tendría que revisarse:

- Se asume que la encargada dispone de un celular o computador con acceso a internet en el local.

- Se asume que el sistema lo usa una sola persona. Si se agregan más usuarios, haría falta definir roles y permisos.

- Se asume que la operación es de un único local. Si se abren más sedes, cambiaría el manejo de inventario y lotes.

- Se asume que los proveedores seguirán emitiendo una factura de compra en cada entrega, y que esa factura es la única constancia de los reclamos.

- Se asume que la encargada registra las ventas en el momento en que ocurren. Si no lo hace, el stock y los lotes dejarían de ser confiables.

- Se asume que el sistema solo registra el medio de pago usado y no se conecta con Nequi, Daviplata ni entidades bancarias.

- Se asume que no se requiere facturación electrónica ni comprobante para el cliente, porque la venta solo genera un registro interno. 

## Evolución previsible del sistema[^c12]

Estas mejoras podrán analizarse e implementarse en el futuro:

- Definir el umbral mínimo de existencias por producto, según su rotación de ventas.

- Definir el umbral mínimo de existencias por producto, según su rotación de ventas.

- Enviar notificaciones push al celular para las alertas de stock, vencimientos y pedidos atrasados.

- Integrar un rol para los vendedores y comparar precios entre productos ofrecidos por los vendedores para ayudar a elegir la mejor cotización.

- Generar reportes de ventas, utilidades, productos más vendidos y pérdidas por vencimiento.

- Administrar los créditos (fiado) con saldos pendientes y recordatorios de pago.

- Sugerir pedidos automáticamente según el stock y el historial de ventas.

- Registrar las devoluciones de clientes y su destino final (desecho o devolución al proveedor).

- Integrarse con facturación electrónica y con plataformas de pago.

- Hacer copias de seguridad automáticas de la información.

# Requisitos específicos[^c13]

En esta sección estarán los requisitos que debe cumplir el sistema a desarrollar.

| Número de requisito | RF 01 |
| --- | --- |
| Nombre de requisito | Iniciar sesión |
| Tipo | Requisito | Restricción |
| Fuente del requisito | Información suministrada por el cliente |
| Prioridad del requisito | Alta/Esencial | Media/Deseado | Baja/ Opcional |

**Descripción.** El sistema permitirá controlar el acceso mediante un inicio de sesión para la dueña del negocio. La información almacenada en la base de datos solo podrá ser consultada por la encargada del local. Se asume que el sistema lo usa una sola persona.

| Número de requisito | RF 02 |
| --- | --- |
| Nombre de requisito | Navegar por el menú |
| Tipo | Requisito | Restricción |
| Fuente del requisito | Información suministrada por el cliente |
| Prioridad del requisito | Alta/Esencial | Media/Deseado | Baja/ Opcional |

**Descripción.** El sistema contará con un menú estructurado que permita el desplazamiento fluido entre los diferentes formularios del sistema. La interfaz debe ser sencilla y adaptarse a un celular o computador.

| Número de requisito | RF 03 |
| --- | --- |
| Nombre de requisito | Gestionar producto |
| Tipo | Requisito | Restricción |
| Fuente del requisito | Información suministrada por el cliente |
| Prioridad del requisito | Alta/Esencial | Media/Deseado | Baja/ Opcional |

**Descripción.** El sistema permitirá registrar, actualizar y consultar los productos que se ofrecen en el local. De cada producto se registran:

- Código y nombre comercial.

- Categoría (bebida, snack/abarrote, lácteo) con una descripción.

- Presentación (botella retornable, plástico desechable, lata, bolsa o caja).

- Precio de compra al proveedor y precio de venta al público, en pesos colombianos (COP).

**Reglas de negocio.**

- Para el precio, se ve cuántas unidades vienen en la caja, se divide el precio de la caja entre esa cantidad para obtener el valor unitario y a ese valor se le suma un 20 o 25 % de utilidad.

- Cuando el producto ya viene con precio sugerido, normalmente se respeta; solo cuando el precio no está escrito en el empaque se le agrega un 20 %.

- Cuando un producto no viene en caja se vende suelto, y el precio depende de cómo se compró.

- Las presentaciones distintas de un mismo producto (por ejemplo, una gaseosa en botella y en lata) se manejan como productos separados; cuando cambia el gramaje, el precio se ajusta hacia arriba o hacia abajo.

- Todos los productos manejan fecha de vencimiento, no solo los lácteos.

- De cada producto se manejan un máximo de 30 unidades disponibles simultáneamente en el local.

| Número de requisito | RF 04 |
| --- | --- |
| Nombre de requisito | Gestionar proveedor |
| Tipo | Requisito | Restricción |
| Fuente del requisito | Información suministrada por el cliente |
| Prioridad del requisito | Alta/Esencial | Media/Deseado | Baja/ Opcional |

**Descripción.** El sistema permitirá registrar y gestionar la información de las aproximadamente 50 empresas proveedoras. De cada proveedor se registran el RUT, la razón social y el teléfono de contacto.

**Reglas de negocio.** Para efectos del sistema no se registran los datos del vendedor: el teléfono del proveedor es suficiente como dato de contacto para reclamos.

| Número de requisito | RF 05 |
| --- | --- |
| Nombre de requisito | Gestionar pedido |
| Tipo | Requisito | Restricción |
| Fuente del requisito | Información suministrada por el cliente |
| Prioridad del requisito | Alta/Esencial | Media/Deseado | Baja/ Opcional |

**Descripción.** El sistema permitirá registrar los pedidos hechos a los proveedores y hacerles seguimiento. De cada pedido se registran la fecha de solicitud, la fecha estimada de entrega y el detalle de lo cotizado (producto, cantidad, precio por unidad y precio acordado en ese momento).

**Reglas de negocio.**

- Una vez cotizado, el pedido no se puede cancelar ni modificar, porque queda pactado y la factura se genera con esa información.

- Si el pedido no llega en la fecha estimada, el sistema debe avisar o marcarlo como atrasado.

- Si un pedido entrante haría que un producto supere el límite de 30 unidades, el sistema debe avisar antes de aceptar la entrega completa.

- Un mismo proveedor puede ofrecer el mismo producto a precios distintos según el vendedor que visite ese día; por lo general se intenta quedarse con el precio más bajo, pero si el producto es de primera necesidad, el precio deja de ser un criterio decisivo.

| Número de requisito | RF 06 |
| --- | --- |
| Nombre de requisito | Gestionar factura de compra |
| Tipo | Requisito | Restricción |
| Fuente del requisito | Información suministrada por el cliente |
| Prioridad del requisito | Alta/Esencial | Media/Deseado | Baja/ Opcional |

**Descripción.** El sistema permitirá registrar las cotizaciones acordadas por pedido y las facturas de compra recibidas. Cuando el vendedor visita el local, cotiza cada producto solicitado indicando su precio por unidad. Días después, al llegar la mercancía, el proveedor emite la factura de compra, de la cual se registran:

- Código de la factura.

- Fecha de emisión y fecha de recepción.

- Detalle de los productos entregados, con su código, nombre, cantidades y precios pactados.

**Reglas de negocio.**

- Los precios pactados en la factura de compra pueden variar respecto al precio de compra habitual del producto.

- La constancia de cualquier reclamo al proveedor es la propia factura de los productos entregados; no se guarda ninguna otra evidencia adicional.

| Número de requisito | RF 07 |
| --- | --- |
| Nombre de requisito | Administrar mercancía recibida |
| Tipo | Requisito | Restricción |
| Fuente del requisito | Información suministrada por el cliente |
| Prioridad del requisito | Alta/Esencial | Media/Deseado | Baja/ Opcional |

**Descripción.** El sistema permitirá registrar la mercancía recibida en lotes independientes por cada entrega, con la cantidad recibida y la fecha de vencimiento. También permitirá registrar y comparar la cantidad facturada por el proveedor con la cantidad efectivamente recibida por la encargada del local, para identificar y documentar discrepancias en el inventario.

**Reglas de negocio.**

- Cada entrega recibida se convierte en un lote independiente.

- Cuando hay una discrepancia entre la factura y lo recibido (producto faltante, distinto o con un sabor diferente al pedido), queda registrada como una nota.

- Si se decide quedarse con un producto distinto al pedido, ese producto entra al sistema como uno nuevo, no como el que originalmente se pidió.

- El máximo de 30 unidades aplica al producto en general y no a cada lote por separado; no es necesario que la suma sea exactamente 30, las unidades sobrantes simplemente se mantienen.

| Número de requisito | RF 08 |
| --- | --- |
| Nombre de requisito | Administrar inventario |
| Tipo | Requisito | Restricción |
| Fuente del requisito | Información suministrada por el cliente |
| Prioridad del requisito | Alta/Esencial | Media/Deseado | Baja/ Opcional |

**Descripción.** El sistema permitirá consultar en todo momento el stock disponible de cada producto y generará alertas visuales cuando un producto alcance su umbral mínimo de existencias o esté próximo a vencer.

**Reglas de negocio.**

- El umbral mínimo de existencias es el mismo número para todos los productos; no varía según qué tan rápido se venda cada uno.

- Un producto está próximo a vencer cuando faltan máximo 5 días para su vencimiento.

- Con que la alerta se vea al abrir la aplicación es suficiente; no se necesita notificación push al celular.

| Número de requisito | RF 09 |
| --- | --- |
| Nombre de requisito | Gestionar ventas |
| Tipo | Requisito | Restricción |
| Fuente del requisito | Información suministrada por el cliente |
| Prioridad del requisito | Alta/Esencial | Media/Deseado | Baja/ Opcional |

**Descripción.** El sistema registrará cada venta mediante una factura interna con la fecha y el monto total pagado, junto con el detalle de los productos vendidos (código, precio unitario y cantidad). La venta se reflejará en la disponibilidad de cada producto y descontará automáticamente la mercancía del lote más antiguo disponible. El sistema debe diferenciar el medio de pago usado en cada venta.

**Reglas de negocio.**

- La salida de mercancía prioriza siempre el lote más antiguo (FIFO).

- El precio de venta es el que está registrado; no se manejan descuentos ni promociones en el mostrador (como 2x1 o combos), salvo la rebaja excepcional por producto próximo a vencer.

- Un producto próximo a vencer se puede comercializar a un precio inferior al recomendado; este descuento se decide caso por caso, ocurre rara vez, y cuando ocurre se vende al precio de compra.

- La mayoría de los pagos son en efectivo, pero también se aceptan transferencias o Nequi/Daviplata, aunque rara vez y solo para compras superiores a $10.000. Estos pagos se registran de forma manual.

- Algunos clientes fieles tienen crédito (fiado) y normalmente pagan dentro de los 5 días siguientes. Solo se registrará el crédito puntual otorgado.

- Las devoluciones de clientes no vuelven al stock: se desechan o se le devuelven al proveedor.

- La factura interna no es una factura electrónica válida ante la DIAN.

| Número de requisito | RF 10 |
| --- | --- |
| Nombre de requisito | Administrar pérdida |
| Tipo | Requisito | Restricción |
| Fuente del requisito | Información suministrada por el cliente |
| Prioridad del requisito | Alta/Esencial | Media/Deseado | Baja/ Opcional |

**Descripción.** El sistema permitirá registrar las pérdidas por mercancía vencida y desechada, indicando cuánto dinero se perdió en la mercancía vencida.

**Reglas de negocio.** Si un producto ya venció, se desecha.

| Número de requisito | RF 11 |
| --- | --- |
| Nombre de requisito | Generar reportes |
| Tipo | Requisito | Restricción |
| Fuente del requisito | Información suministrada por el cliente |
| Prioridad del requisito | Alta/Esencial | Media/Deseado | Baja/ Opcional |

**Descripción.** El sistema permitirá consultar los siguientes reportes:

- Ventas del día.

- Productos más vendidos.

- Ganancia del mes.

- Productos próximos a vencer.

## Requisitos comunes de los interfaces[^c14]

En esta parte estarán todas las entradas y salidas del sistema.

### Interfaces de usuario[^c15]

La interfaz del sistema debe ser sencilla, estar completamente en español y adaptarse tanto a un celular como a un computador. Su apariencia sigue la identidad empresarial de la Cigarrería Alcalá:

		- Colores: rojo como color primario, amarillo/naranja como color secundario y blanco/gris claro como color neutro. Las alertas de stock mínimo y de productos próximos a vencer usan colores distintivos (amarillo y rojo).

		- Tipografía: los encabezados y el nombre de la marca usan una tipografía redondeada y amigable (por ejemplo, Poppins o Nunito). El cuerpo del texto y los datos numéricos (precios, cantidades y tablas de inventario) usan una de alta legibilidad (por ejemplo, Inter o Roboto).

		- Distribución: en pantallas pequeñas, los módulos se muestran en una sola columna con navegación por pestañas inferiores (venta, inventario, proveedores y reportes). En pantallas grandes se distribuyen en un panel lateral fijo junto al detalle de la venta en curso.

		- Alertas: se muestran de forma visual al abrir la aplicación.

[Insertar imagen: logo e imagotipo de la Cigarrería Alcalá]

- Interfaz principal:

[Insertar imagen]

Esta interfaz trata sobre el menú principal del sistema, desde el cual la usuaria accede a los módulos de venta, inventario, proveedores y reportes, y donde se muestran las alertas al abrir la aplicación.

- Interfaz de inventario:

[Insertar imagen]

Esta interfaz trata sobre el stock disponible de cada producto. Resalta con colores los productos que alcanzaron el umbral mínimo de existencias o que están próximos a vencer.

- Interfaz de detalle de lote:

[Insertar imagen]

Esta interfaz trata sobre el detalle de los lotes de un producto. Se abre al tocar un producto en el inventario (por ejemplo, la leche próxima a vencer) y muestra la cantidad recibida, la fecha de vencimiento y las unidades disponibles de cada lote.

### Interfaces de hardware[^c16]

- Celular:

Es el dispositivo principal desde el que la usuaria opera el sistema. Debe contar con pantalla táctil, navegador web actualizado y conexión a internet por Wi-Fi. La interfaz se adapta al tamaño de la pantalla en orientación vertical y no requiere instalar software adicional.

- Computador o tablet:

Puede ubicarse en el mostrador para registrar ventas y entradas de mercancía. Debe contar con navegador web actualizado y conexión a internet. Se maneja con teclado y mouse (o pantalla táctil en la tablet), y la interfaz aprovecha el espacio adicional de la pantalla.

El cliente no especificó la necesidad de conectar el sistema con otros dispositivos (escáner de códigos, cámara o impresora). La venta solo genera un registro interno, no un comprobante impreso.

### Interfaces de software[^c17]

El cliente no especificó la necesidad de que el sistema deba conectarse a algún componente de software. Por tratarse de un producto independiente (ver 2.1), no se integra con otros productos de software. El único software requerido en los dispositivos es un navegador web.

Quedan fuera de esta fase la integración con plataformas de pago (Nequi, Daviplata y PSE), la facturación electrónica ante la DIAN y la exportación de reportes a Excel o PDF (ver Alcance y Evolución previsible).

### Interfaces de comunicación[^c18]

- Internet:

El sistema es una aplicación web. El navegador del dispositivo se comunica con el servidor a través de internet, mediante la red Wi-Fi del local, usando el protocolo HTTPS para proteger los datos que se envían, como la contraseña y la información del negocio.

El sistema no se comunica con otros sistemas: no se conecta con bancos, plataformas de pago, la DIAN ni sistemas de los proveedores.

## Requisitos funcionales[^c19]

A continuación, se presentará los requisitos funcionales del sistema:

### Gestión de producto-8 EN MODO CASO DE USO

El sistema permitirá registrar y consultar los productos. (esto no, sino una descripcion segun lo requerido, sera largo)

### Requisito funcional 2

El sistema permitirá registrar y consultar proveedores.

### Requisito funcional 3

### Requisito funcional n

## Requisitos no funcionales

### Requisitos de rendimiento [^c20]

- El sistema deberá garantizar la realización de transacciones en menos de 2 segundos.

- El sistema deberá registrar una venta o una entrada de mercancía en menos de 2 segundos en el 95% de las transacciones, con un usuario conectado a la vez.

- El sistema deberá mostrar las consultas de stock y los reportes (ventas del día, productos más vendidos, ganancia del mes y productos próximos a vencer) en menos de 3 segundos en el 95% de los casos.

### Seguridad[^c21]

		- El sistema deberá asignar un modulo de inicio de sesión que garantice el acceso autorizado en un 99%.

		- El sistema deberá garantizar el rechazo del 99% de los intentos de acceso sin credenciales válidas mediante una contraseña cifrada.

		- El sistema deberá cerrar la sesión automáticamente tras 10 minutos de inactividad, porque el dispositivo puede quedar a la vista en el mostrador.

### Fiabilidad[^c22]

		- El sistema deberá presentar como máximo 1 incidente al mes que impida registrar ventas o entradas de mercancía.

		- El sistema deberá guardar cada venta o entrada de mercancía completa o no guardarla (0 registros parciales).

### Disponibilidad[^c23]

- El software deberá estar disponible al menos 12 horas al día.

### Mantenibilidad[^c24]

- El desarrollador deberá realizar un mantenimiento mensualmente en cuanto a la base de datos para verificar si soporta la cantidad de registros y solicitudes hechas al día por mes.

### Portabilidad[^c25]

- El sistema deberá garantizar la portabilidad del sistema en un celular en un 95%.

## Otros requisitos[^c26]

[Inserte aquí el texto]

# Apéndices

[Inserte aquí el texto]

Pueden contener todo tipo de información relevante para la SRS pero que, propiamente, no forme parte de la SRS.

- DIAGRAMA DE CONTEXTO DE SU APLICATIVO

- Metodología de desarrollo tradicional que aplicarían para el desarrollo de su aplicativo (justificando su selección)

- Metodología de desarrollo ágil que aplicarían para el desarrollo de su aplicativo (justificando su selección)

- Prototipo del sistema

- Anexos:

- Anexar los recursos de recolección de información, utilizados para elaborar la narrativa del proyecto.

- Formatos que utiliza la entidad o empresa que se toma como base para el desarrollo del sistema.

|  |  | Descripción de requisitos del sofware |
| --- | --- | --- |

|  |  | Descripción de requisitos del sofware |
| --- | --- | --- |

|  |  | Descripción de requisitos del sofware |
| --- | --- | --- |

|  |  | Descripción de requisitos del sofware |
| --- | --- | --- |
