from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from database.conexion import SessionLocal
from keyboards.menu import menu_principal
from services.usuario_service import UsuarioService

router = Router()


async def mostrar_menu_principal(
    message: Message,
):
    await message.answer(
        f"👋 Bienvenido <b>{message.from_user.full_name}</b>\n\n"
        "Seleccione una opción del menú.",
        reply_markup=menu_principal,
    )


@router.message(CommandStart())
async def comando_start(message: Message):
    db = SessionLocal()

    try:
        UsuarioService.registrar_si_no_existe(
            db=db,
            telegram_user=message.from_user,
        )

        await mostrar_menu_principal(message)

    finally:
        db.close()