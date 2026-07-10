from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String


from database.conexion import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
    )

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    username: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    language_code: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )



    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    tiendas = relationship(
        "Tienda",
        back_populates="usuario",

    )

