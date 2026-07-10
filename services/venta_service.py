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