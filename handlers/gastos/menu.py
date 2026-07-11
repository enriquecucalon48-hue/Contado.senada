from aiogram import Router, F
from aiogram.types import Message

from keyboards.gastos import menu_gastos

router = Router()


@router.message(F.text == "💸 Gastos")
async def menu_gastos_handler(message: Message):
    await message.answer(
        "💸 Módulo de Gastos",
        reply_markup=menu_gastos,
    )