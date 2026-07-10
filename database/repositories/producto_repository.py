from sqlalchemy.orm import Session

from database.models.producto import Producto


class ProductoRepository:

    @staticmethod
    def crear(
        db: Session,
        nombre: str,
        precio: float,
        stock: int,
        tienda_id: int,
    ):
        producto = Producto(
            nombre=nombre,
            precio=precio,
            stock=stock,
            tienda_id=tienda_id,
        )

        db.add(producto)
        db.commit()
        db.refresh(producto)

        return producto

    @staticmethod
    def listar(db: Session, tienda_id: int):
        return (
            db.query(Producto)
            .filter(
                Producto.tienda_id == tienda_id,
                Producto.activo == True,
            )
            .order_by(Producto.nombre)
            .all()
        )
    @staticmethod
    def obtener_por_id(
        db: Session,
        producto_id: int,
    ):
        return (
            db.query(Producto)
            .filter(
                Producto.id == producto_id,
                Producto.activo == True,
            )
            .first()
        )

    @staticmethod
    def actualizar(
        db: Session,
        producto: Producto,
        precio: float,
        stock: int,
    ):
        producto.precio = precio
        producto.stock = stock

        db.commit()
        db.refresh(producto)

        return producto

    @staticmethod
    def eliminar(
        db: Session,
        producto: Producto,
    ):
        producto.activo = False

        db.commit()