from aiogram import Router, F
from aiogram.types import Message

from database.conexion import SessionLocal
from services.gasto_service import GastoService

router = Router()


@router.message(F.text == "📋 Ver gastos")
async def listar_gastos(message: Message):
    db = SessionLocal()

    try:
        gastos = GastoService.listar(db)

        if not gastos:
            await message.answer(
                "📭 No existen gastos registrados."
            )
            return

        texto = "💸 <b>Historial de gastos</b>\n\n"

        total = 0

        for i, gasto in enumerate(
            gastos,
            start=1,
        ):
            texto += (
                f"{i}. 📝 {gasto.concepto}\n"
                f"📂 {gasto.categoria}\n"
                f"💵 ${float(gasto.monto):.2f}\n"
                f"📅 {gasto.fecha.strftime('%d/%m/%Y %H:%M')}\n\n"
            )

            total += float(gasto.monto)

        texto += (
            "━━━━━━━━━━━━━━━━━━\n"
            f"💸 Total gastos: ${total:.2f}"
        )

        await message.answer(texto)

    finally:
        db.close()