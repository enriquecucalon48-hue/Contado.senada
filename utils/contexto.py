from aiogram.types import Message

from database.repositories.usuario_repository import UsuarioRepository
from database.repositories.tienda_repository import TiendaRepository


def obtener_usuario_actual(db, message: Message):
    return UsuarioRepository.obtener_por_telegram_id(
        db,
        message.from_user.id,
    )


def obtener_tienda_actual(db, usuario_id: int):
    tiendas = TiendaRepository.obtener_por_usuario(
        db,
        usuario_id,
    )

    if not tiendas:
        return None

    return tiendas[0]