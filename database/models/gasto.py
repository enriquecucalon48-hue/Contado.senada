from datetime import datetime

from sqlalchemy import DateTime, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from database.conexion import Base


class Gasto(Base):
    __tablename__ = "gastos"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    concepto: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    categoria: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Otros",
    )

    monto: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    fecha: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )