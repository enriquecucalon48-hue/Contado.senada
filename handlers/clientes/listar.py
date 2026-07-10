from aiogram import Router, F
from aiogram.types import Message

from database.conexion import SessionLocal
from services.cliente_service import ClienteService
from utils.contexto import (
    obtener_usuario_actual,
    obtener_tienda_actual,
)

router = Router()


@router.message(F.text == "📋 Ver clientes")
async def listar_clientes(message: Message):
    db = SessionLocal()

    try:
        usuario = obtener_usuario_actual(db, message)

        if usuario is None:
            await message.answer("❌ Usuario no encontrado.")
            return

        tienda = obtener_tienda_actual(db, usuario.id)

        if tienda is None:
            await message.answer("❌ No tienes una tienda creada.")
            return

        clientes = ClienteService.listar(
            db=db,
            tienda_id=tienda.id,
        )

        if not clientes:
            await message.answer(
                "👥 No hay clientes registrados."
            )
            return

        texto = "👥 <b>Clientes</b>\n\n"

        for i, cliente in enumerate(clientes, start=1):
            texto += (
                f"{i}. <b>{cliente.nombre}</b>\n"
                f"📞 {cliente.telefono or '-'}\n"
                f"🪪 {cliente.cedula or '-'}\n\n"
            )

        await message.answer(texto)

    finally:
        db.close()