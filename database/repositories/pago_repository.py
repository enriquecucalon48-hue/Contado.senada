from sqlalchemy import func
from sqlalchemy.orm import Session

from database.models.pago import Pago
from database.models.venta import Venta


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
        total = (
            db.query(
                func.coalesce(
                    func.sum(Pago.monto),
                    0,
                )
            )
            .filter(
                Pago.venta_id == venta_id,
            )
            .scalar()
        )

        return float(total)

    @staticmethod
    def saldo_pendiente(
        db: Session,
        venta_id: int,
    ):
        venta = db.get(
            Venta,
            venta_id,
        )

        if venta is None:
            return 0

        total_pagado = PagoRepository.total_pagado(
            db,
            venta_id,
        )

        return float(venta.total) - total_pagado