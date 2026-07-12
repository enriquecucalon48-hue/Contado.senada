from sqlalchemy.orm import Session

from database.models.tienda import Tienda


class TiendaRepository:

    @staticmethod
    def obtener_por_usuario(db: Session, usuario_id: int):
        return (
            db.query(Tienda)
            .filter(Tienda.usuario_id == usuario_id)
            .all()
        )

    @staticmethod
    def crear(
        db: Session,
        nombre: str,
        direccion: str | None,
        telefono: str | None,
        usuario_id: int,
    ):
        tienda = Tienda(
            nombre=nombre,
            direccion=direccion,
            telefono=telefono,
            usuario_id=usuario_id,
        )

        db.add(tienda)
        db.commit()
        db.refresh(tienda)

        return tienda

    @staticmethod
    def eliminar(
        db: Session,
        tienda: Tienda,
    ):
        db.delete(tienda)
        db.commit()