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
    datos = await state.get_data()

    ventas = datos["ventas"]

    try:
        indice = int(message.text) - 1
    except ValueError:
        await message.answer(
            "❌ Debes escribir un número."
        )
        return

    if indice < 0 or indice >= len(ventas):
        await message.answer(
            "❌ Esa venta no existe."
        )
        return

    venta = ventas[indice]

    db = SessionLocal()

    try:
        venta = VentaService.obtener_por_id(
            db=db,
            venta_id=venta.id,
        )

        if venta is None:
            await message.answer(
                "❌ Venta no encontrada."
            )
            return

        texto = (
            f"🧾 <b>Venta #{venta.id}</b>\n\n"
            f"👤 Cliente: {venta.cliente.nombre}\n"
            f"📅 {venta.fecha.strftime('%d/%m/%Y %H:%M')}\n\n"
            "────────────────\n\n"
        )

        for detalle in venta.detalles:

            texto += (
                f"📦 {detalle.producto.nombre}\n"
                f"{detalle.cantidad} x "
                f"${detalle.precio_unitario} = "
                f"${detalle.subtotal}\n\n"
            )

        texto += (
            "────────────────\n\n"
            f"💰 <b>Total: ${venta.total}</b>"
        )

        await message.answer(texto)

    finally:
        db.close()

    await state.clear()