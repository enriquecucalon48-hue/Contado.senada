from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.conexion import SessionLocal
from database.repositories.usuario_repository import UsuarioRepository
from database.repositories.tienda_repository import TiendaRepository
from services.producto_service import ProductoService
from states.producto_states import EliminarProducto

router = Router()


@router.message(F.text == "🗑 Eliminar producto")
async def eliminar_producto(message: Message, state: FSMContext):

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

        texto = "🗑 Escribe el número del producto que deseas eliminar.\n\n"

        for i, producto in enumerate(productos, start=1):
            texto += f"{i}. {producto.nombre}\n"

        await state.update_data(productos=productos)

        await state.set_state(EliminarProducto.seleccionar)

        await message.answer(texto)

    finally:
        db.close()


@router.message(EliminarProducto.seleccionar)
async def confirmar_eliminacion(message: Message, state: FSMContext):

    datos = await state.get_data()

    productos = datos["productos"]

    try:
        indice = int(message.text) - 1
    except ValueError:
        await message.answer("❌ Debes escribir un número.")
        return

    if indice < 0 or indice >= len(productos):
        await message.answer("❌ Producto no válido.")
        return

    producto = productos[indice]

    db = SessionLocal()

    try:
        producto_db = ProductoService.obtener_por_id(
            db=db,
            producto_id=producto.id,
        )

        if producto_db is None:
            await message.answer("❌ Producto no encontrado.")
            return

        ProductoService.eliminar(
            db=db,
            producto=producto_db,
        )

        await message.answer(
            f"🗑 Producto <b>{producto.nombre}</b> eliminado correctamente."
        )

    finally:
        db.close()

    await state.clear()