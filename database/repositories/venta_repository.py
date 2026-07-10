from sqlalchemy.orm import Session

from database.models.venta import Venta
from database.models.venta_detalle import VentaDetalle
from database.models.producto import Producto


class VentaRepository:

    @staticmethod
    def crear(
        db: Session,
        cliente_id: int,
        tienda_id: int,
        productos: list,
    ):
        venta = Venta(
            cliente_id=cliente_id,
            tienda_id=tienda_id,
            total=0,
        )

        db.add(venta)
        db.flush()

        total = 0

        for item in productos:
            producto = db.get(
                Producto,
                item["producto_id"],
            )

            if producto is None:
                raise ValueError("Producto no encontrado.")

            if producto.stock < item["cantidad"]:
                raise ValueError(
                    f"Stock insuficiente para {producto.nombre}"
                )

            subtotal = producto.precio * item["cantidad"]

            detalle = VentaDetalle(
                venta_id=venta.id,
                producto_id=producto.id,
                cantidad=item["cantidad"],
                precio_unitario=producto.precio,
                subtotal=subtotal,
            )

            db.add(detalle)

            producto.stock -= item["cantidad"]

            total += subtotal

        venta.total = total

        db.commit()

        db.refresh(venta)

        return venta