from sqlalchemy.orm import Session

from database.models.cliente import Cliente


class ClienteRepository:

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
        cliente = Cliente(
            nombre=nombre,
            cedula=cedula,
            telefono=telefono,
            direccion=direccion,
            correo=correo,
            tienda_id=tienda_id,
        )

        db.add(cliente)
        db.commit()
        db.refresh(cliente)

        return cliente

    @staticmethod
    def listar(
        db: Session,
        tienda_id: int,
    ):
        return (
            db.query(Cliente)
            .filter(
                Cliente.tienda_id == tienda_id,
                Cliente.activo == True,
            )
            .order_by(Cliente.nombre)
            .all()
        )

    @staticmethod
    def obtener_por_id(
        db: Session,
        cliente_id: int,
    ):
        return (
            db.query(Cliente)
            .filter(
                Cliente.id == cliente_id,
                Cliente.activo == True,
            )
            .first()
        )

    @staticmethod
    def actualizar(
        db: Session,
        cliente: Cliente,
        nombre: str,
        cedula: str | None,
        telefono: str | None,
        direccion: str | None,
        correo: str | None,
    ):
        cliente.nombre = nombre
        cliente.cedula = cedula
        cliente.telefono = telefono
        cliente.direccion = direccion
        cliente.correo = correo

        db.commit()
        db.refresh(cliente)

        return cliente

    @staticmethod
    def eliminar(
        db: Session,
        cliente: Cliente,
    ):
        cliente.activo = False

        db.commit()