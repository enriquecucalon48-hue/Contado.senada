from sqlalchemy.orm import Session

from database.models.usuario import Usuario


class UsuarioRepository:

    @staticmethod
    def obtener_por_telegram_id(db: Session, telegram_id: int):
        return (
            db.query(Usuario)
            .filter(Usuario.telegram_id == telegram_id)
            .first()
        )

    @staticmethod
    def crear(
        db: Session,
        telegram_id: int,
        nombre: str,
        username: str | None,
        language_code: str |None,
    ):
        usuario = Usuario(
            telegram_id=telegram_id,
            nombre=nombre,
            username=username,
            language_code=language_code,
        )

        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        return usuario

    @staticmethod
    def obtener_id_por_telegram(db: Session, telegram_id: int):
        return (
            db.query(Usuario)
            .filter(Usuario.telegram_id == telegram_id)
            .first()
        )