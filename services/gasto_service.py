from sqlalchemy.orm import Session

from database.repositories.gasto_repository import (
    GastoRepository,
)


class GastoService:

    @staticmethod
    def crear(
        db: Session,
        concepto: str,
        categoria: str,
        monto: float,
    ):
        if monto <= 0:
            raise ValueError(
                "El monto debe ser mayor que cero."
            )

        return GastoRepository.crear(
            db=db,
            concepto=concepto,
            categoria=categoria,
            monto=monto,
        )

    @staticmethod
    def listar(
        db: Session,
    ):
        return GastoRepository.listar(db)

    @staticmethod
    def obtener_por_id(
        db: Session,
        gasto_id: int,
    ):
        return GastoRepository.obtener_por_id(
            db,
            gasto_id,
        )

    @staticmethod
    def eliminar(
        db: Session,
        gasto,
    ):
        return GastoRepository.eliminar(
            db,
            gasto,
        )

    @staticmethod
    def listar(
            db: Session,
    ):
        return GastoRepository.listar(db)