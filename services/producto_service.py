from sqlalchemy.orm import Session

from database.repositories.producto_repository import ProductoRepository


class ProductoService:

    @staticmethod
    def crear(
        db: Session,
        nombre: str,
        precio: float,
        stock: int,
        tienda_id: int,
    ):
        return ProductoRepository.crear(
            db=db,
            nombre=nombre,
            precio=precio,
            stock=stock,
            tienda_id=tienda_id,
        )

    @staticmethod
    def listar(
        db: Session,
        tienda_id: int,
    ):
        return ProductoRepository.listar(
            db=db,
            tienda_id=tienda_id,
        )

    @staticmethod
    def obtener_por_id(
        db: Session,
        producto_id: int,
    ):
        return ProductoRepository.obtener_por_id(
            db=db,
            producto_id=producto_id,
        )

    @staticmethod
    def actualizar(
        db: Session,
        producto,
        precio: float,
        stock: int,
    ):
        return ProductoRepository.actualizar(
            db=db,
            producto=producto,
            precio=precio,
            stock=stock,
        )

    @staticmethod
    def eliminar(
        db: Session,
        producto,
    ):
        return ProductoRepository.eliminar(
            db=db,
            producto=producto,
        )