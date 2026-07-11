from sqlalchemy.orm import Session

from database.repositories.pago_repository import PagoRepository


class PagoService:

    @staticmethod
    def crear(
        db: Session,
        venta_id: int,
        monto: float,
    ):
        return PagoRepository.crear(
            db=db,
            venta_id=venta_id,
            monto=monto,
        )

    @staticmethod
    def listar_por_venta(
        db: Session,
        venta_id: int,
    ):
        return PagoRepository.listar_por_venta(
            db=db,
            venta_id=venta_id,
        )

    @staticmethod
    def total_pagado(
        db: Session,
        venta_id: int,
    ):
        return PagoRepository.total_pagado(
            db=db,
            venta_id=venta_id,
        )