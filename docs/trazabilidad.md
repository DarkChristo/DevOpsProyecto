# Matriz de trazabilidad

| Requisito | Prioridad | Criterios de aceptación | Prueba | Verificación |
|---|---|---|---|---|
| RF-01 Iniciar sesión | Alta | Credenciales inválidas son rechazadas; La sesión se cierra tras 10 min de inactividad | — | revision |
| RF-02 Navegar por el menú | Media | Menú accesible desde celular y computador | — | revision |
| RF-03 Gestionar producto | Alta | Cada producto tiene categoría y presentación; Presentaciones distintas son productos separados | test_rf03_producto_requiere_categoria | automatica |
| RF-04 Gestionar proveedor | Alta | El RUT identifica de forma única al proveedor | test_rf04_rut_unico | automatica |
| RF-05 Gestionar pedido | Alta | El pedido guarda fecha estimada de entrega; El detalle guarda cantidad, precio cotizado y precio acordado; Se avisa si una entrega haría superar 30 unidades | test_rf05_aviso_limite_30 | automatica |
| RF-06 Gestionar factura de compra | Alta | La factura queda asociada a un pedido; Guarda fecha de emisión y de recepción | test_rf06_factura_requiere_pedido | automatica |
| RF-07 Administrar mercancía recibida | Alta | Cada lote guarda cantidad recibida y fecha de vencimiento | test_rf07_lote_con_vencimiento | automatica |
| RF-08 Administrar inventario | Alta | El stock es recibido menos salidas; Se alertan lotes que vencen en máximo 5 días | test_rf08_stock_derivado | automatica |
| RF-09 Gestionar ventas | Alta | La salida respeta FIFO; Cada venta registra el medio de pago; Una línea de venta puede tomar de más de un lote | test_rf09_fifo | automatica |
| RF-10 Administrar pérdida | Alta | La pérdida se calcula con el precio de compra de lo desechado | test_rf10_perdida_vencimiento | automatica |
| RF-11 Generar reportes | Media | Existe el reporte de próximos a vencer | — | revision |

# Requisitos no funcionales medibles

| ID | Requisito | Meta | Cómo se verifica |
|---|---|---|---|
| RNF-01 | Rendimiento de transacciones | Registrar venta o entrada en menos de 2 s en el 95 % de los casos | medición de tiempos (prueba de carga) |
| RNF-02 | Rendimiento de consultas | Consultas y reportes en menos de 3 s en el 95 % de los casos | medición de tiempos |
| RNF-03 | Seguridad de acceso | Cierre de sesión tras 10 minutos de inactividad | prueba automática de sesión |
| RNF-04 | Fiabilidad | 0 registros parciales por venta o entrada | prueba automática de transacciones |
| RNF-05 | Disponibilidad | Disponible al menos 12 horas al día | monitoreo de disponibilidad |
| RNF-06 | Mantenibilidad | 1 revisión de la base de datos por mes | tarea programada y registro |
