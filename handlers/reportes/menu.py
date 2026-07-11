from aiogram import Router, F
from aiogram.types import Message

from keyboards.reportes import menu_reportes

router = Router()


@router.message(F.text == "📊 Reportes")
async def menu_reportes_handler(message: Message):
    await message.answer(
        "📊 Módulo de Reportes",
        reply_markup=menu_reportes,
    )