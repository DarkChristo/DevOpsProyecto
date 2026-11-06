"""Pruebas de aceptación: cada criterio del SRS se convierte en una prueba sobre el esquema (SQLite en memoria)."""
import sqlite3, pathlib, unittest
SCHEMA = (pathlib.Path(__file__).resolve().parent.parent / "db" / "schema.sql").read_text(encoding="utf-8")

class Base(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.db.executescript(SCHEMA)
        self.db.executescript("""
        INSERT INTO Categoria VALUES (1,'Bebida','Gaseosas y jugos');
        INSERT INTO Producto VALUES (10,'Gaseosa lata',1,'lata',1500,2000);
        INSERT INTO Proveedor VALUES ('900123-4','Distribuidora Sur','3001112222');
        INSERT INTO Pedido VALUES (1,'900123-4','2026-10-01','2026-10-05');
        INSERT INTO DetallePedido VALUES (1,10,40,1500,1500);
        INSERT INTO FacturaCompra VALUES (1,1,'2026-10-04','2026-10-04');
        INSERT INTO FacturaCompra VALUES (2,1,'2026-10-10','2026-10-10');
        """)
    def q(self, sql, *a): return self.db.execute(sql, a).fetchall()
    def lote(self, id_, factura, cant, venc):
        self.db.execute("INSERT INTO Inventario VALUES (?,?,?,?,?)", (id_, 10, factura, cant, venc))

class TestAceptacion(Base):
    def test_rf03_producto_requiere_categoria(self):  # RF-03
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("INSERT INTO Producto VALUES (11,'Sin categoría',99,'lata',1,2)")

    def test_rf04_rut_unico(self):  # RF-04
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("INSERT INTO Proveedor VALUES ('900123-4','Otra','3')")

    def test_rf05_aviso_limite_30(self):  # RF-05: el sistema avisa si el stock superaría 30
        self.lote(1, 1, 20, '2027-01-01'); self.lote(2, 2, 15, '2027-02-01')
        self.assertEqual(self.q("SELECT CodProducto, Stock FROM v_exceso_30"), [(10, 35)])

    def test_rf06_factura_requiere_pedido(self):  # RF-06
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("INSERT INTO FacturaCompra VALUES (9,999,'2026-10-10','2026-10-10')")

    def test_rf07_lote_con_vencimiento(self):  # RF-07
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("INSERT INTO Inventario VALUES (1,10,1,5,NULL)")

    def test_rf08_stock_derivado(self):  # RF-08: stock = recibido - salidas, sin columna redundante
        self.lote(1, 1, 20, '2027-01-01')
        self.db.executescript("""
        INSERT INTO FacturaVenta VALUES (1,'2026-10-12','EFECTIVO');
        INSERT INTO DetalleVenta VALUES (1,1,10,3,2000);
        INSERT INTO Movimiento VALUES (1,1,1,'VENTA',3,'2026-10-12');""")
        self.assertEqual(self.q("SELECT Stock FROM v_stock_actual WHERE CodProducto=10"), [(17,)])

    def test_rf09_fifo(self):  # RF-09: sale primero el lote recibido antes; si se agota, pasa al siguiente
        self.lote(1, 1, 5, '2027-03-01'); self.lote(2, 2, 10, '2027-01-01')
        self.assertEqual(self.q("SELECT IdInventario FROM v_lote_fifo WHERE CodProducto=10 AND Orden=1"), [(1,)])
        self.db.executescript("""
        INSERT INTO FacturaVenta VALUES (1,'2026-10-12','NEQUI');
        INSERT INTO DetalleVenta VALUES (1,1,10,8,2000);
        INSERT INTO Movimiento VALUES (1,1,1,'VENTA',5,'2026-10-12');
        INSERT INTO Movimiento VALUES (2,2,1,'VENTA',3,'2026-10-12');""")  # una línea toma de 2 lotes
        self.assertEqual(self.q("SELECT IdInventario, Disponible FROM v_lote_fifo WHERE CodProducto=10"), [(2, 7)])
        with self.assertRaises(sqlite3.IntegrityError):  # medio de pago obligatorio y válido
            self.db.execute("INSERT INTO FacturaVenta VALUES (2,'2026-10-12','TRUEQUE')")

    def test_rf10_perdida_vencimiento(self):  # RF-10: pérdida = unidades desechadas × precio de compra
        self.lote(1, 1, 10, '2026-10-01')
        self.db.execute("INSERT INTO Movimiento VALUES (1,1,NULL,'VENCIMIENTO',4,'2026-10-02')")
        self.assertEqual(self.q("SELECT PerdidaCOP FROM v_perdida_vencimiento"), [(6000.0,)])

if __name__ == "__main__":
    unittest.main()
