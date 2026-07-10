from aiogram import Router, F
from aiogram.types import Message

from keyboards.ventas import teclado_ventas

router = Router()


@router.message(F.text == "🧾 Ventas")
async def menu_ventas(message: Message):
    await message.answer(
        "🧾 <b>Módulo de Ventas</b>\n\n"
        "Selecciona una opción:",
        reply_markup=teclado_ventas,
    )