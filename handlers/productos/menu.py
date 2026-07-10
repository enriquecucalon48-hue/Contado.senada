from aiogram import Router, F
from aiogram.types import Message

from keyboards.productos import teclado_productos

router = Router()


@router.message(F.text == "📦 Productos")
async def menu_productos_handler(message: Message):
    await message.answer(
        "📦 <b>Módulo de Productos</b>\n\n"
        "Selecciona una opción:",
        reply_markup=teclado_productos,
    )