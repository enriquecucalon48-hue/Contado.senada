from aiogram import Router, F
from aiogram.types import Message

from database.conexion import SessionLocal
from services.reporte_service import ReporteService

router = Router()


@router.message(F.text == "💳 Clientes con deuda")
async def clientes_con_deuda(message: Message):
    db = SessionLocal()

    try:
        clientes = ReporteService.clientes_con_deuda(
            db=db,
        )

        if not clientes:
            await message.answer(
                "✅ No existen clientes con deuda."
            )
            return

        texto = "💳 <b>Clientes con deuda</b>\n\n"

        total_deuda = 0

        for i, cliente in enumerate(
            clientes,
            start=1,
        ):
            texto += (
                f"{i}. 👤 {cliente['cliente'].nombre}\n"
                f"💰 Compró: ${cliente['vendido']:.2f}\n"
                f"💵 Pagó: ${cliente['pagado']:.2f}\n"
                f"💳 Debe: ${cliente['deuda']:.2f}\n\n"
            )

            total_deuda += cliente["deuda"]

        texto += (
            "━━━━━━━━━━━━━━━━━━\n"
            f"💵 Total por cobrar: ${total_deuda:.2f}"
        )

        await message.answer(texto)

    finally:
        db.close()