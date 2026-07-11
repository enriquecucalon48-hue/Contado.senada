from sqlalchemy.orm import Session

from database.repositories.reporte_repository import (
    ReporteRepository,
)


class ReporteService:

    @staticmethod
    def total_clientes(
        db: Session,
    ):
        return ReporteRepository.total_clientes(db)

    @staticmethod
    def total_productos(
        db: Session,
    ):
        return ReporteRepository.total_productos(db)

    @staticmethod
    def total_ventas(
        db: Session,
    ):
        return ReporteRepository.total_ventas(db)

    @staticmethod
    def ventas_hoy(
        db: Session,
    ):
        return ReporteRepository.ventas_hoy(db)

    @staticmethod
    def ventas_mes(
        db: Session,
    ):
        return ReporteRepository.ventas_mes(db)

    @staticmethod
    def productos_stock_bajo(
        db: Session,
    ):
        return ReporteRepository.productos_stock_bajo(db)

    @staticmethod
    def saldo_pendiente(
        db: Session,
    ):
        return ReporteRepository.saldo_pendiente(db)


    @staticmethod
    def clientes_con_deuda(
        db: Session,
    ):
        return ReporteRepository.clientes_con_deuda(
            db=db,
        )