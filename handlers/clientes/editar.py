from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.conexion import SessionLocal
from services.cliente_service import ClienteService
from states.cliente_states import EditarCliente
from utils.contexto import (
    obtener_usuario_actual,
    obtener_tienda_actual,
)

router = Router()


@router.message(F.text == "✏️ Editar cliente")
async def editar_cliente(message: Message, state: FSMContext):
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
            await message.answer("👥 No existen clientes.")
            return

        texto = "✏️ Escribe el número del cliente que deseas editar.\n\n"

        for i, cliente in enumerate(clientes, start=1):
            texto += f"{i}. {cliente.nombre}\n"

        await state.update_data(clientes=clientes)
        await state.set_state(EditarCliente.seleccionar)

        await message.answer(texto)

    finally:
        db.close()


@router.message(EditarCliente.seleccionar)
async def seleccionar_cliente(message: Message, state: FSMContext):
    datos = await state.get_data()

    clientes = datos["clientes"]

    try:
        indice = int(message.text) - 1
    except ValueError:
        await message.answer("❌ Debes escribir un número.")
        return

    if indice < 0 or indice >= len(clientes):
        await message.answer("❌ Ese cliente no existe.")
        return

    cliente = clientes[indice]

    await state.update_data(cliente_id=cliente.id)

    await state.set_state(EditarCliente.nombre)

    await message.answer(
        f"👤 Nombre actual: {cliente.nombre}\n\n"
        "Escribe el nuevo nombre:"
    )


@router.message(EditarCliente.nombre)
async def editar_nombre(message: Message, state: FSMContext):
    await state.update_data(nombre=message.text)

    await state.set_state(EditarCliente.cedula)

    await message.answer("🪪 Nueva cédula (o -):")


@router.message(EditarCliente.cedula)
async def editar_cedula(message: Message, state: FSMContext):
    cedula = None if message.text == "-" else message.text

    await state.update_data(cedula=cedula)

    await state.set_state(EditarCliente.telefono)

    await message.answer("📞 Nuevo teléfono (o -):")


@router.message(EditarCliente.telefono)
async def editar_telefono(message: Message, state: FSMContext):
    telefono = None if message.text == "-" else message.text

    await state.update_data(telefono=telefono)

    await state.set_state(EditarCliente.direccion)

    await message.answer("📍 Nueva dirección (o -):")


@router.message(EditarCliente.direccion)
async def editar_direccion(message: Message, state: FSMContext):
    direccion = None if message.text == "-" else message.text

    await state.update_data(direccion=direccion)

    await state.set_state(EditarCliente.correo)

    await message.answer("📧 Nuevo correo (o -):")


@router.message(EditarCliente.correo)
async def editar_correo(message: Message, state: FSMContext):
    correo = None if message.text == "-" else message.text

    await state.update_data(correo=correo)

    datos = await state.get_data()

    db = SessionLocal()

    try:
        cliente = ClienteService.obtener_por_id(
            db=db,
            cliente_id=datos["cliente_id"],
        )

        if cliente is None:
            await message.answer("❌ Cliente no encontrado.")
            return

        ClienteService.actualizar(
            db=db,
            cliente=cliente,
            nombre=datos["nombre"],
            cedula=datos["cedula"],
            telefono=datos["telefono"],
            direccion=datos["direccion"],
            correo=correo,
        )

        await message.answer(
            "✅ Cliente actualizado correctamente."
        )

    finally:
        db.close()

    await state.clear()