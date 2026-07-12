from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers.start import mostrar_menu_principal

router = Router()


@router.message(F.text == "⬅️ Menú principal")
async def volver(
    message: Message,
    state: FSMContext,
):
    await state.clear()

    await mostrar_menu_principal(message)


@router.message(F.text == "🏠 Inicio")
async def inicio(
    message: Message,
    state: FSMContext,
):
    await state.clear()

    await mostrar_menu_principal(message)