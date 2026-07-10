from sqlalchemy.orm import Session

from database.repositories.venta_repository import VentaRepository


class VentaService:

    @staticmethod
    def crear(
        db: Session,
        cliente_id: int,
        tienda_id: int,
        productos: list,
    ):
        return VentaRepository.crear(
            db=db,
            cliente_id=cliente_id,
            tienda_id=tienda_id,
            productos=productos,
        )

    @staticmethod
    def listar(
        db: Session,
        tienda_id: int,
    ):
        return VentaRepository.listar(
            db=db,
            tienda_id=tienda_id,
        )

    @staticmethod
    def obtener_por_id(
        db: Session,
        venta_id: int,
    ):
        return VentaRepository.obtener_por_id(
            db=db,
            venta_id=venta_id,
        )