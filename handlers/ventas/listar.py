from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message

from database.conexion import SessionLocal
from services.venta_service import VentaService
from utils.contexto import (
    obtener_usuario_actual,
    obtener_tienda_actual,
)

router = Router()


@router.message(
    StateFilter("*"),
    F.text == "📋 Ver ventas",
)
async def listar_ventas(message: Message):
    db = SessionLocal()

    try:
        usuario = obtener_usuario_actual(
            db,
            message,
        )

        if usuario is None:
            await message.answer(
                "❌ Usuario no encontrado."
            )
            return

        tienda = obtener_tienda_actual(
            db,
            usuario.id,
        )

        if tienda is None:
            await message.answer(
                "❌ No tienes una tienda creada."
            )
            return

        ventas = VentaService.listar(
            db=db,
            tienda_id=tienda.id,
        )

        if not ventas:
            await message.answer(
                "🧾 No existen ventas registradas."
            )
            return

        texto = "🧾 <b>Ventas registradas</b>\n\n"

        for i, venta in enumerate(ventas, start=1):
            texto += (
                f"{i}. Venta #{venta.id}\n"
                f"💰 Total: ${venta.total}\n"
                f"📅 {venta.fecha.strftime('%d/%m/%Y %H:%M')}\n\n"
            )

        await message.answer(texto)

    finally:
        db.close()