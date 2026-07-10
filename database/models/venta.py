from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.conexion import Base


class Venta(Base):
    __tablename__ = "ventas"

    id: Mapped[int] = mapped_column(primary_key=True)

    fecha: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    total: Mapped[float] = mapped_column(
        Numeric(10, 2),
        default=0,
    )

    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id"),
        nullable=False,
    )

    tienda_id: Mapped[int] = mapped_column(
        ForeignKey("tiendas.id"),
        nullable=False,
    )

    cliente = relationship(
        "Cliente",
        back_populates="ventas",
    )

    tienda = relationship(
        "Tienda",
        back_populates="ventas",
    )

    detalles = relationship(
        "VentaDetalle",
        back_populates="venta",
        cascade="all, delete-orphan",
    )