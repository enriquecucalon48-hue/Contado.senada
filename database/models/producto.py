from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.conexion import Base


class Producto(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(primary_key=True)

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    precio: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    stock: Mapped[int] = mapped_column(
        default=0,
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    tienda_id: Mapped[int] = mapped_column(
        ForeignKey("tiendas.id"),
        nullable=False,
    )

    tienda = relationship(
        "Tienda",
        back_populates="productos",
    )