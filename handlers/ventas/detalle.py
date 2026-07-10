from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.conexion import SessionLocal
from services.venta_service import VentaService
from states.venta_states import VerVenta

router = Router()


@router.message(VerVenta.seleccionar)
async def ver_detalle_venta(
    message: Message,
    state: FSMContext,
):
    print(">>> Entró a detalle")

    datos = await state.get_data()

    ventas = datos["ventas"]

    indice = int(message.text) - 1

    venta = ventas[indice]

    print(f"Venta seleccionada: {venta.id}")

    await message.answer("Detalle funcionando")

    await state.clear()