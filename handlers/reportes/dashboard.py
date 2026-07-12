from aiogram import Router, F
from aiogram.types import Message

from database.conexion import SessionLocal
from services.reporte_service import ReporteService

router = Router()


@router.message(F.text == "📊 Dashboard")
async def dashboard(message: Message):
    db = SessionLocal()

    try:
        clientes = ReporteService.total_clientes(db)
        productos = ReporteService.total_productos(db)
        ventas = ReporteService.total_ventas(db)

        ventas_hoy = ReporteService.ventas_hoy(db)
        ventas_mes = ReporteService.ventas_mes(db)

        stock_bajo = ReporteService.productos_stock_bajo(db)
        saldo = ReporteService.saldo_pendiente(db)

        texto = (
            "📊 <b>CONTADO.SENADA v2</b>\n"
            "━━━━━━━━━━━━━━━━━━\n\n"

            f"👥 Clientes: <b>{clientes}</b>\n"
            f"📦 Productos: <b>{productos}</b>\n"
            f"🧾 Ventas: <b>{ventas}</b>\n\n"

            f"💰 Ventas de hoy: <b>${float(ventas_hoy):.2f}</b>\n"
            f"📅 Ventas del mes: <b>${float(ventas_mes):.2f}</b>\n\n"

           
            f"💳 Saldo por cobrar: <b>${saldo:.2f}</b>"
        )

        await message.answer(texto)

    finally:
        db.close()