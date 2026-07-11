from aiogram import Router, F
from aiogram.types import Message

from database.conexion import SessionLocal
from services.caja_service import CajaService

router = Router()


@router.message(F.text == "💰 Caja")
async def ver_caja(message: Message):
    db = SessionLocal()

    try:
        resumen = CajaService.resumen(db)

        texto = (
            "💰 <b>CAJA</b>\n\n"

            f"💵 Ingresos\n"
            f"${resumen['ingresos']:.2f}\n\n"

            f"💸 Gastos\n"
            f"${resumen['gastos']:.2f}\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            f"💰 Balance\n"
            f"${resumen['balance']:.2f}"
        )

        await message.answer(texto)

    finally:
        db.close()