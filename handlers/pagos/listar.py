from aiogram import Router, F
from aiogram.types import Message

from database.conexion import SessionLocal
from services.pago_service import PagoService
from services.venta_service import VentaService
from utils.contexto import (
    obtener_usuario_actual,
    obtener_tienda_actual,
)

router = Router()


@router.message(F.text == "📋 Historial de pagos")
async def historial_pagos(message: Message):
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
                "🧾 No existen ventas."
            )
            return

        texto = "📜 <b>Historial de pagos</b>\n\n"

        for venta in ventas:

            pagos = PagoService.listar_por_venta(
                db=db,
                venta_id=venta.id,
            )

            total_pagado = PagoService.total_pagado(
                db=db,
                venta_id=venta.id,
            )

            saldo = PagoService.saldo_pendiente(
                db=db,
                venta_id=venta.id,
            )

            texto += (
                f"🧾 Venta #{venta.id}\n"
                f"💰 Total: ${float(venta.total):.2f}\n"
                f"💵 Pagado: ${total_pagado:.2f}\n"
                f"💳 Saldo: ${saldo:.2f}\n\n"
            )

            if not pagos:
                texto += "Sin pagos registrados.\n\n"
                continue

            for pago in pagos:
                texto += (
                    f"• ${float(pago.monto):.2f}"
                    f" - {pago.fecha.strftime('%d/%m/%Y %H:%M')}\n"
                )

            texto += "\n"

        await message.answer(texto)

    finally:
        db.close()