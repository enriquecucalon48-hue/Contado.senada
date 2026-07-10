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

        texto = "✏️ Escribe el número del producto que deseas editar.\n\n"

        for i, producto in enumerate(productos, start=1):
            texto += f"{i}. {producto.nombre}\n"

        await state.update_data(productos=productos)
        await state.set_state(EditarProducto.seleccionar)

        await message.answer(texto)

    finally:
        db.close()


@router.message(EditarProducto.seleccionar)
async def seleccionar_producto(message: Message, state: FSMContext):
    datos = await state.get_data()

    productos = datos["productos"]

    try:
        indice = int(message.text) - 1
    except ValueError:
        await message.answer("❌ Debes escribir un número.")
        return

    if indice < 0 or indice >= len(productos):
        await message.answer("❌ Ese producto no existe.")
        return

    producto = productos[indice]

    await state.update_data(
        producto_id=producto.id,
    )

    await state.set_state(EditarProducto.precio)

    await message.answer(
        f"💲 Precio actual: ${producto.precio}\n\n"
        "Escribe el nuevo precio:"
    )


@router.message(EditarProducto.precio)
async def nuevo_precio(message: Message, state: FSMContext):
    try:
        precio = float(message.text)
    except ValueError:
        await message.answer("❌ Ingresa un precio válido.")
        return

    await state.update_data(
        precio=precio,
    )

    await state.set_state(EditarProducto.stock)

    await message.answer(
        "📦 Escribe el nuevo stock:"
    )

@router.message(EditarProducto.stock)
async def nuevo_stock(message: Message, state: FSMContext):
    try:
        stock = int(message.text)
    except ValueError:
        await message.answer("❌ Ingresa un stock válido.")
        return

    datos = await state.get_data()

    db = SessionLocal()

    try:
        producto = ProductoService.obtener_por_id(
            db=db,
            producto_id=datos["producto_id"],
        )

        if producto is None:
            await message.answer("❌ Producto no encontrado.")
            return

        ProductoService.actualizar(
            db=db,
            producto=producto,
            precio=datos["precio"],
            stock=stock,
        )

        await message.answer(
            "✅ Producto actualizado correctamente."
        )

    finally:
        db.close()

    await state.clear()