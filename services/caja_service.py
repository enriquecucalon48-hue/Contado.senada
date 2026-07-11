from sqlalchemy.orm import Session

from database.repositories.caja_repository import CajaRepository


class CajaService:

    @staticmethod
    def resumen(
        db: Session,
    ):
        ingresos = CajaRepository.total_ingresos(db)

        gastos = CajaRepository.total_gastos(db)

        return {
            "ingresos": ingresos,
            "gastos": gastos,
            "balance": ingresos - gastos,
        }