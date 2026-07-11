from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.menu import menu_principal

router = Router()


@router.message(F.text == "⬅️ Menú principal")
async def volver(
    message: Message,
    state: FSMContext,
):
    await state.clear()

    await message.answer(
        "🏠 Menú principal",
        reply_markup=menu_principal,
    )


@router.message(F.text == "🏠 Inicio")
async def inicio(
    message: Message,
    state: FSMContext,
):
    await state.clear()

    await message.answer(
        "🏠 Menú principal",
        reply_markup=menu_principal,
    )