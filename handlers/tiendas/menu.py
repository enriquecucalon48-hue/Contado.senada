from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.tiendas import menu_tiendas

router = Router()


@router.message(F.text == "🏪 Tiendas")
async def mostrar_menu_tiendas(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        "🏪 <b>Módulo de Tiendas</b>\n\n"
        "Selecciona una opción:",
        reply_markup=menu_tiendas,
    )