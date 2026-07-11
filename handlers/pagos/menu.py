from aiogram import Router, F
from aiogram.types import Message

from keyboards.pagos import menu_pagos

router = Router()


@router.message(F.text == "💵 Pagos")
async def menu(message: Message):
    await message.answer(
        "💵 <b>Módulo de Pagos</b>",
        reply_markup=menu_pagos,
    )