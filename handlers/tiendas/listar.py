from aiogram import Router, F
from aiogram.types import Message

from database.conexion import SessionLocal
from services.tienda_service import TiendaService
from utils.contexto import obtener_usuario_actual

router = Router()


@router.message(F.text == "📋 Ver tiendas")
async def listar_tiendas(message: Message):
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

        tiendas = TiendaService.listar(
            db=db,
            usuario_id=usuario.id,
        )

        if not tiendas:
            await message.answer(
                "🏪 No tienes tiendas registradas."
            )
            return

        texto = "🏪 <b>Mis tiendas</b>\n\n"

        for i, tienda in enumerate(
            tiendas,
            start=1,
        ):
            texto += (
                f"{i}. <b>{tienda.nombre}</b>\n"
                f"📍 {tienda.direccion or 'Sin dirección'}\n"
                f"📞 {tienda.telefono or 'Sin teléfono'}\n\n"
            )

        await message.answer(texto)

    finally:
        db.close()