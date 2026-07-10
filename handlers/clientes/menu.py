from aiogram import Router, F
from aiogram.types import Message

from keyboards.clientes import teclado_clientes

router = Router()


@router.message(F.text == "👥 Clientes")
async def menu_clientes(message: Message):
    await message.answer(
        "👥 <b>Módulo de Clientes</b>\n\n"
        "Selecciona una opción:",
        reply_markup=teclado_clientes,
    )