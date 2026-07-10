from aiogram import Router, F
from aiogram.types import Message

from database.conexion import SessionLocal
from database.repositories.usuario_repository import UsuarioRepository
from database.repositories.tienda_repository import TiendaRepository
from services.producto_service import ProductoService

router = Router()


@router.message(F.text == "📋 Ver productos")
async def listar_productos(message: Message):
    db = SessionLocal()

    try:
        usuario = UsuarioRepository.obtener_por_telegram_id(
            db,
            message.from_user.id,
        )

        if usuario is None:
            await message.answer("❌ Usuario no encontrado.")
            return

        tiendas = TiendaRepository.obtener_por_usuario(
            db,
            usuario.id,
        )

        if not tiendas:
            await message.answer(
                "❌ No tienes ninguna tienda creada."
            )
            return

        tienda = tiendas[0]

        productos = ProductoService.listar(
            db=db,
            tienda_id=tienda.id,
        )

        if not productos:
            await message.answer(
                "📦 No hay productos registrados."
            )
            return

        texto = "📦 <b>Productos</b>\n\n"

        for i, producto in enumerate(productos, start=1):
            texto += (
                f"{i}. <b>{producto.nombre}</b>\n"
                f"💲 Precio: ${producto.precio}\n"
                f"📦 Stock: {producto.stock}\n\n"
            )

        await message.answer(texto)

    finally:
        db.close()