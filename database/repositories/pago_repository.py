from sqlalchemy.orm import Session

from database.models.pago import Pago


class PagoRepository:

    @staticmethod
    def crear(
        db: Session,
        venta_id: int,
        monto: float,
    ):
        pago = Pago(
            venta_id=venta_id,
            monto=monto,
        )

        db.add(pago)

        db.commit()

        db.refresh(pago)

        return pago

    @staticmethod
    def listar_por_venta(
        db: Session,
        venta_id: int,
    ):
        return (
            db.query(Pago)
            .filter(
                Pago.venta_id == venta_id,
            )
            .order_by(
                Pago.fecha.desc(),
            )
            .all()
        )

    @staticmethod
    def total_pagado(
        db: Session,
        venta_id: int,
    ):
        pagos = (
            db.query(Pago)
            .filter(
                Pago.venta_id == venta_id,
            )
            .all()
        )

        return sum(
            pago.monto
            for pago in pagos
        )