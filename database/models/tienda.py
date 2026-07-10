from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.conexion import Base


class Tienda(Base):
    __tablename__ = "tiendas"

    id: Mapped[int] = mapped_column(primary_key=True)

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    direccion: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    telefono: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False,
    )

    usuario = relationship(
        "Usuario",
        back_populates="tiendas",

    )
    productos = relationship(
        "Producto",
        back_populates="tienda",
        cascade="all, delete-orphan",
    )

    clientes = relationship(
        "Cliente",
        back_populates="tienda",
        cascade="all, delete-orphan",
    )

