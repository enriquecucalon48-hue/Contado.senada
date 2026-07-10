from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.conexion import SessionLocal
from services.cliente_service import ClienteService
from utils.contexto import (
    obtener_usuario_actual,
    obtener_tienda_actual,
)
from states.venta_states import NuevaVenta
from services.venta_service import VentaService
router = Router()


@router.message(F.text == "➕ Nueva venta")
async def nueva_venta(message: Message, state: FSMContext):
    db = SessionLocal()

    try:
        usuario = obtener_usuario_actual(db, message)

        if usuario is None:
            await message.answer(
                "❌ Usuario no encontrado."
            )
            return

        tienda = obtener_tienda_actual(
            db,
            usuario.id,
        )

        if tienda is None:
            await message.answer(
                "❌ No tienes una tienda creada."
            )
            return

        clientes = ClienteService.listar(
            db=db,
            tienda_id=tienda.id,
        )

        if not clientes:
            await message.answer(
                "👥 No existen clientes registrados."
            )
            return

        texto = "👥 Selecciona el cliente.\n\n"

        for i, cliente in enumerate(clientes, start=1):
            texto += f"{i}. {cliente.nombre}\n"

        await state.clear()

        await state.update_data(
            clientes=clientes,
            carrito=[],
        )

        await state.set_state(
            NuevaVenta.cliente
        )

        await message.answer(texto)

    finally:
        db.close()

from services.producto_service import ProductoService


@router.message(NuevaVenta.cliente)
async def seleccionar_cliente(message: Message, state: FSMContext):
    datos = await state.get_data()

    clientes = datos["clientes"]

    try:
        indice = int(message.text) - 1
    except ValueError:
        await message.answer("❌ Debes escribir un número.")
        return

    if indice < 0 or indice >= len(clientes):
        await message.answer("❌ Cliente no válido.")
        return

    cliente = clientes[indice]

    await state.update_data(
        cliente_id=cliente.id,
        cliente_nombre=cliente.nombre,
    )

    db = SessionLocal()

    try:
        usuario = obtener_usuario_actual(db, message)

        tienda = obtener_tienda_actual(
            db,
            usuario.id,
        )

        productos = ProductoService.listar(
            db=db,
            tienda_id=tienda.id,
        )

        if not productos:
            await message.answer(
                "📦 No existen productos registrados."
            )
            return

        texto = "📦 Selecciona un producto.\n\n"

        for i, producto in enumerate(productos, start=1):
            texto += (
                f"{i}. {producto.nombre} "
                f"(${producto.precio}) "
                f"Stock: {producto.stock}\n"
            )

        await state.update_data(
            productos=productos,
        )

        await state.set_state(
            NuevaVenta.producto
        )

        await message.answer(texto)

    finally:
        db.close()

@router.message(NuevaVenta.producto)
async def seleccionar_producto(message: Message, state: FSMContext):
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

    await state.update_data(
        producto_id=producto.id,
        producto_nombre=producto.nombre,
        producto_precio=float(producto.precio),
    )

    await state.set_state(NuevaVenta.cantidad)

    await message.answer(
        f"📦 Producto: <b>{producto.nombre}</b>\n"
        f"💲 Precio: ${producto.precio}\n"
        f"📦 Stock: {producto.stock}\n\n"
        "Escribe la cantidad:"
    )



@router.message(NuevaVenta.cantidad)
async def agregar_al_carrito(message: Message, state: FSMContext):
    try:
        cantidad = int(message.text)
    except ValueError:
        await message.answer("❌ Debes escribir un número.")
        return

    if cantidad <= 0:
        await message.answer("❌ La cantidad debe ser mayor que cero.")
        return

    datos = await state.get_data()

    carrito = datos.get("carrito", [])

    subtotal = datos["producto_precio"] * cantidad

    carrito.append(
        {
            "producto_id": datos["producto_id"],
            "nombre": datos["producto_nombre"],
            "precio": datos["producto_precio"],
            "cantidad": cantidad,
            "subtotal": subtotal,
        }
    )

    total = sum(item["subtotal"] for item in carrito)

    await state.update_data(carrito=carrito)

    texto = "🛒 <b>Carrito</b>\n\n"

    for i, item in enumerate(carrito, start=1):
        texto += (
            f"{i}. {item['nombre']}\n"
            f"   {item['cantidad']} x ${item['precio']} = ${item['subtotal']:.2f}\n\n"
        )

    texto += (
        "──────────────\n"
        f"💰 <b>Total:</b> ${total:.2f}\n\n"
        "Escribe:\n"
        "1️⃣ Agregar otro producto\n"
        "2️⃣ Confirmar venta"
    )

    await state.set_state(NuevaVenta.carrito)

    await message.answer(texto)

@router.message(NuevaVenta.carrito)
async def decidir_carrito(message: Message, state: FSMContext):
    if message.text == "1":
        datos = await state.get_data()

        productos = datos["productos"]

        texto = "📦 Selecciona otro producto.\n\n"

        for i, producto in enumerate(productos, start=1):
            texto += (
                f"{i}. {producto.nombre} "
                f"(${producto.precio}) "
                f"Stock: {producto.stock}\n"
            )

        await state.set_state(
            NuevaVenta.producto
        )

        await message.answer(texto)

        return

    if message.text == "2":
        await state.set_state(
            NuevaVenta.confirmar
        )

        await confirmar_venta(
            message,
            state,
        )

        return

    await message.answer(
        "❌ Escribe 1 o 2."
    )


@router.message(NuevaVenta.confirmar)
async def confirmar_venta(message: Message, state: FSMContext):
    datos = await state.get_data()

    db = SessionLocal()

    try:
        usuario = obtener_usuario_actual(
            db,
            message,
        )

        tienda = obtener_tienda_actual(
            db,
            usuario.id,
        )

        productos = []

        for item in datos["carrito"]:
            productos.append(
                {
                    "producto_id": item["producto_id"],
                    "cantidad": item["cantidad"],
                }
            )

        venta = VentaService.crear(
            db=db,
            cliente_id=datos["cliente_id"],
            tienda_id=tienda.id,
            productos=productos,
        )

        await message.answer(
            f"✅ Venta #{venta.id} registrada correctamente."
        )

    except Exception as e:
        await message.answer(
            f"❌ Error:\n{e}"
        )

    finally:
        db.close()

    await state.clear()


