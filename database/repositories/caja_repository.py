from sqlalchemy import func
from sqlalchemy.orm import Session

from database.models.gasto import Gasto
from database.models.pago import Pago


class CajaRepository:

    @staticmethod
    def total_ingresos(
        db: Session,
    ):
        total = (
            db.query(
                func.coalesce(
                    func.sum(Pago.monto),
                    0,
                )
            )
            .scalar()
        )

        return float(total)

    @staticmethod
    def total_gastos(
        db: Session,
    ):
        total = (
            db.query(
                func.coalesce(
                    func.sum(Gasto.monto),
                    0,
                )
            )
            .scalar()
        )

        return float(total)