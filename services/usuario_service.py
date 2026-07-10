from sqlalchemy.orm import Session

from database.repositories.usuario_repository import UsuarioRepository


class UsuarioService:

    @staticmethod
    def registrar_si_no_existe(db: Session, telegram_user):

        usuario = UsuarioRepository.obtener_por_telegram_id(
            db,
            telegram_user.id
        )

        if usuario:
            return usuario

        return UsuarioRepository.crear(
            db=db,
            telegram_id=telegram_user.id,
            nombre=telegram_user.full_name,
            username=telegram_user.username,
            language_code=telegram_user.language_code,
        )