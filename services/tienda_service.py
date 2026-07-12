from sqlalchemy.orm import Session

from database.repositories.tienda_repository import TiendaRepository


class TiendaService:

    @staticmethod
    def listar(db: Session, usuario_id: int):
        return TiendaRepository.obtener_por_usuario(
            db=db,
            usuario_id=usuario_id,
        )

    @staticmethod
    def crear(
        db: Session,
        nombre: str,
        direccion: str | None,
        telefono: str | None,
        usuario_id: int,
    ):
        return TiendaRepository.crear(
            db=db,
            nombre=nombre,
            direccion=direccion,
            telefono=telefono,
            usuario_id=usuario_id,
        )
    @staticmethod
    def eliminar(
        db: Session,
        tienda,
    ):
        TiendaRepository.eliminar(
            db=db,
            tienda=tienda,
        )