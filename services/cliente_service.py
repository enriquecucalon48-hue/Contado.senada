from sqlalchemy.orm import Session

from database.repositories.cliente_repository import ClienteRepository


class ClienteService:

    @staticmethod
    def crear(
        db: Session,
        nombre: str,
        cedula: str | None,
        telefono: str | None,
        direccion: str | None,
        correo: str | None,
        tienda_id: int,
    ):
        return ClienteRepository.crear(
            db=db,
            nombre=nombre,
            cedula=cedula,
            telefono=telefono,
            direccion=direccion,
            correo=correo,
            tienda_id=tienda_id,
        )

    @staticmethod
    def listar(
        db: Session,
        tienda_id: int,
    ):
        return ClienteRepository.listar(
            db=db,
            tienda_id=tienda_id,
        )

    @staticmethod
    def obtener_por_id(
        db: Session,
        cliente_id: int,
    ):
        return ClienteRepository.obtener_por_id(
            db=db,
            cliente_id=cliente_id,
        )

    @staticmethod
    def actualizar(
        db: Session,
        cliente,
        nombre: str,
        cedula: str | None,
        telefono: str | None,
        direccion: str | None,
        correo: str | None,
    ):
        return ClienteRepository.actualizar(
            db=db,
            cliente=cliente,
            nombre=nombre,
            cedula=cedula,
            telefono=telefono,
            direccion=direccion,
            correo=correo,
        )

    @staticmethod
    def eliminar(
        db: Session,
        cliente,
    ):
        return ClienteRepository.eliminar(
            db=db,
            cliente=cliente,
        )