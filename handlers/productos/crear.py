from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states.producto_states import CrearProducto

from database.conexion import SessionLocal
from database.repositories.usuario_repository import UsuarioRepository
from database.repositories.tienda_repository import TiendaRepository
from services.producto_service import ProductoService






router = Router()


@router.message(F.text == "➕ Nuevo producto")
async def nuevo_producto(message: Message, state: FSMContext):
    await state.set_state(CrearProducto.nombre)

    await message.answer(
        "📝 Escribe el nombre del producto:"
    )


@router.message(CrearProducto.nombre)
async def recibir_nombre(message: Message, state: FSMContext):
    await state.update_data(nombre=message.text)

    await state.set_state(CrearProducto.precio)

    await message.answer(
        "💲 Escribe el precio:"
    )


@router.message(CrearProducto.precio)
async def recibir_precio(message: Message, state: FSMContext):
    try:
        precio = float(message.text.replace(",", "."))

    except ValueError:
        await message.answer(
            "❌ Debes escribir un número.\n\nEjemplo:\n15.50"
        )
        return

    await state.update_data(precio=precio)

    await state.set_state(CrearProducto.stock)

    await message.answer(
        "📦 Stock inicial:"
    )


@router.message(CrearProducto.stock)
async def recibir_stock(message: Message, state: FSMContext):
    try:
        stock = int(message.text)

    except ValueError:
        await message.answer(
            "❌ Debes escribir un número entero."
        )
        return

    await state.update_data(stock=stock)

    datos = await state.get_data()

    db = SessionLocal()

    try:
        # Buscar usuario
        usuario = UsuarioRepository.obtener_por_telegram_id(
            db,
            message.from_user.id,
        )

        if not usuario:
            await message.answer("❌ Usuario no encontrado.")
            return

        # Buscar tiendas del usuario
        tiendas = TiendaRepository.obtener_por_usuario(
            db,
            usuario.id,
        )

        if not tiendas:
            await message.answer(
                "❌ Primero debes crear una tienda."
            )
            return

        # Usamos la primera tienda
        tienda = tiendas[0]

        ProductoService.crear(
            db=db,
            nombre=datos["nombre"],
            precio=datos["precio"],
            stock=stock,
            tienda_id=tienda.id,
        )

        await message.answer(
            f"""
✅ <b>Producto creado correctamente</b>

📦 Nombre: {datos['nombre']}
💲 Precio: ${datos['precio']:.2f}
📦 Stock: {stock}
""",
            parse_mode="HTML",
        )

    finally:
        db.close()

    await state.clear()

