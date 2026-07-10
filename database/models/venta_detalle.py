from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.conexion import Base


class VentaDetalle(Base):
    __tablename__ = "venta_detalles"

    id: Mapped[int] = mapped_column(primary_key=True)

    venta_id: Mapped[int] = mapped_column(
        ForeignKey("ventas.id"),
        nullable=False,
    )

    producto_id: Mapped[int] = mapped_column(
        ForeignKey("productos.id"),
        nullable=False,
    )

    cantidad: Mapped[int] = mapped_column(
        nullable=False,
    )

    precio_unitario: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    subtotal: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    venta = relationship(
        "Venta",
        back_populates="detalles",
    )

    producto = relationship("Producto")