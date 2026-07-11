from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.conexion import Base


class Pago(Base):
    __tablename__ = "pagos"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    fecha: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    monto: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    venta_id: Mapped[int] = mapped_column(
        ForeignKey("ventas.id"),
        nullable=False,
    )

    venta = relationship(
        "Venta",
        back_populates="pagos",
    )