from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.conexion import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True)

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    cedula: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    telefono: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    direccion: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    correo: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
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
        back_populates="clientes",
    )