from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.conexion import SessionLocal
from database.repositories.usuario_repository import UsuarioRepository
from database.repositories.tienda_repository import TiendaRepository
from services.producto_service import ProductoService
from states.producto_states import EditarProducto

router = Router()


@router.message(F.text == "✏️ Editar producto")
async def editar_producto(message: Message, state: FSMContext):

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
            await message.answer("❌ No tienes tiendas.")
            return

        tienda = tiendas[0]

        productos = ProductoService.listar(
            db=db,
            tienda_id=tienda.id,
        )

        if not productos:
            await message.answer("📦 No existen productos.")
            return

        texto = "✏️ Escribe el número del producto.\n\n"

        for i, producto in enumerate(productos, start=1):
            texto += f"{i}. {producto.nombre}\n"

        await state.update_data(productos=productos)

        await state.set_state(EditarProducto.seleccionar)

        await message.answer(texto)

    finally:
        db.close()