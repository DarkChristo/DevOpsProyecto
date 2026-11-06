-- Esquema de DEMOSTRACIÓN derivado de la Entrega 3 (Normalización, 3FN).
-- Ajustar al MER final del equipo. Stock, total de venta y "atrasado" son DERIVADOS (vistas), no columnas.
PRAGMA foreign_keys = ON;

CREATE TABLE Categoria (CodCate INTEGER PRIMARY KEY, NombreCate TEXT NOT NULL, DescripCate TEXT);
CREATE TABLE Producto (
  CodProducto INTEGER PRIMARY KEY, NombreProd TEXT NOT NULL,
  CodCate INTEGER NOT NULL REFERENCES Categoria(CodCate),
  Presentacion TEXT NOT NULL, PrecioCompra REAL NOT NULL CHECK (PrecioCompra >= 0),
  PrecioVenta REAL NOT NULL CHECK (PrecioVenta >= 0));
CREATE TABLE Proveedor (RutProv TEXT PRIMARY KEY, RazonSocial TEXT NOT NULL, TelefonoP TEXT NOT NULL);
CREATE TABLE Pedido (
  IdPedido INTEGER PRIMARY KEY, RutProv TEXT NOT NULL REFERENCES Proveedor(RutProv),
  FechaPedido TEXT NOT NULL, FechaEstimadaEntrega TEXT NOT NULL);
CREATE TABLE DetallePedido (
  IdPedido INTEGER NOT NULL REFERENCES Pedido(IdPedido),
  CodProducto INTEGER NOT NULL REFERENCES Producto(CodProducto),
  Cantidad INTEGER NOT NULL CHECK (Cantidad > 0),
  PrecioUnitarioCotizado REAL NOT NULL, PrecioAcordado REAL NOT NULL,
  PRIMARY KEY (IdPedido, CodProducto));
CREATE TABLE FacturaCompra (
  IdFacturaC INTEGER PRIMARY KEY, IdPedido INTEGER NOT NULL REFERENCES Pedido(IdPedido),
  FechaEmision TEXT NOT NULL, FechaRecepcion TEXT NOT NULL);
-- Inventario = lote (cada línea entregada es un lote con su vencimiento)
CREATE TABLE Inventario (
  IdInventario INTEGER PRIMARY KEY,
  CodProducto INTEGER NOT NULL REFERENCES Producto(CodProducto),
  IdFacturaC INTEGER NOT NULL REFERENCES FacturaCompra(IdFacturaC),
  CantidadRecibida INTEGER NOT NULL CHECK (CantidadRecibida > 0),
  FechaVencimiento TEXT NOT NULL);
CREATE TABLE FacturaVenta (
  IdFacturaV INTEGER PRIMARY KEY, Fecha TEXT NOT NULL,
  MedioPago TEXT NOT NULL CHECK (MedioPago IN ('EFECTIVO','TRANSFERENCIA','NEQUI','DAVIPLATA')));
CREATE TABLE DetalleVenta (
  IdDetalleV INTEGER PRIMARY KEY, IdFacturaV INTEGER NOT NULL REFERENCES FacturaVenta(IdFacturaV),
  CodProducto INTEGER NOT NULL REFERENCES Producto(CodProducto),
  Cantidad INTEGER NOT NULL CHECK (Cantidad > 0), PrecioUnitario REAL NOT NULL);
-- Salidas de lote: por venta o por vencimiento (una línea de venta puede tomar de varios lotes: 1:M)
CREATE TABLE Movimiento (
  IdMov INTEGER PRIMARY KEY,
  IdInventario INTEGER NOT NULL REFERENCES Inventario(IdInventario),
  IdDetalleV INTEGER REFERENCES DetalleVenta(IdDetalleV),
  TipoMov TEXT NOT NULL CHECK (TipoMov IN ('VENTA','VENCIMIENTO')),
  CantidadM INTEGER NOT NULL CHECK (CantidadM > 0), FechaMov TEXT NOT NULL,
  CHECK ((TipoMov='VENTA' AND IdDetalleV IS NOT NULL) OR (TipoMov='VENCIMIENTO' AND IdDetalleV IS NULL)));

-- Derivados
CREATE VIEW v_lote_disponible AS
SELECT i.IdInventario, i.CodProducto, i.FechaVencimiento, i.IdFacturaC,
       i.CantidadRecibida - COALESCE((SELECT SUM(m.CantidadM) FROM Movimiento m WHERE m.IdInventario=i.IdInventario),0) AS Disponible
FROM Inventario i;

CREATE VIEW v_stock_actual AS
SELECT p.CodProducto, p.NombreProd, COALESCE(SUM(l.Disponible),0) AS Stock
FROM Producto p LEFT JOIN v_lote_disponible l ON l.CodProducto=p.CodProducto GROUP BY p.CodProducto;

-- FIFO: lote más antiguo (por fecha de recepción) con disponible > 0
CREATE VIEW v_lote_fifo AS
SELECT l.CodProducto, l.IdInventario, l.Disponible, l.FechaVencimiento,
       ROW_NUMBER() OVER (PARTITION BY l.CodProducto ORDER BY fc.FechaRecepcion, l.IdInventario) AS Orden
FROM v_lote_disponible l JOIN FacturaCompra fc ON fc.IdFacturaC=l.IdFacturaC
WHERE l.Disponible > 0;

CREATE VIEW v_exceso_30 AS SELECT * FROM v_stock_actual WHERE Stock > 30;

CREATE VIEW v_proximo_vencer AS
SELECT * FROM v_lote_disponible
WHERE Disponible > 0 AND julianday(FechaVencimiento) - julianday(date('now')) BETWEEN 0 AND 5;

CREATE VIEW v_perdida_vencimiento AS
SELECT COALESCE(SUM(m.CantidadM * p.PrecioCompra),0) AS PerdidaCOP
FROM Movimiento m JOIN Inventario i ON i.IdInventario=m.IdInventario
JOIN Producto p ON p.CodProducto=i.CodProducto WHERE m.TipoMov='VENCIMIENTO';
