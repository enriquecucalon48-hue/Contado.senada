from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.conexion import SessionLocal
from services.cliente_service import ClienteService
from states.cliente_states import CrearCliente
from utils.contexto import (
    obtener_usuario_actual,
    obtener_tienda_actual,
)

router = Router()


@router.message(F.text == "➕ Nuevo cliente")
async def nuevo_cliente(message: Message, state: FSMContext):
    await state.set_state(CrearCliente.nombre)

    await message.answer(
        "👤 Escribe el nombre del cliente:"
    )


@router.message(CrearCliente.nombre)
async def recibir_nombre(message: Message, state: FSMContext):
    await state.update_data(nombre=message.text)

    await state.set_state(CrearCliente.cedula)

    await message.answer(
        "🪪 Cédula (o escribe -):"
    )


@router.message(CrearCliente.cedula)
async def recibir_cedula(message: Message, state: FSMContext):
    cedula = None if message.text == "-" else message.text

    await state.update_data(cedula=cedula)

    await state.set_state(CrearCliente.telefono)

    await message.answer(
        "📞 Teléfono (o escribe -):"
    )


@router.message(CrearCliente.telefono)
async def recibir_telefono(message: Message, state: FSMContext):
    telefono = None if message.text == "-" else message.text

    await state.update_data(telefono=telefono)

    await state.set_state(CrearCliente.direccion)

    await message.answer(
        "📍 Dirección (o escribe -):"
    )


@router.message(CrearCliente.direccion)
async def recibir_direccion(message: Message, state: FSMContext):
    direccion = None if message.text == "-" else message.text

    await state.update_data(direccion=direccion)

    await state.set_state(CrearCliente.correo)

    await message.answer(
        "📧 Correo (o escribe -):"
    )


@router.message(CrearCliente.correo)
async def recibir_correo(message: Message, state: FSMContext):
    correo = None if message.text == "-" else message.text

    await state.update_data(correo=correo)

    datos = await state.get_data()

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

        ClienteService.crear(
            db=db,
            nombre=datos["nombre"],
            cedula=datos["cedula"],
            telefono=datos["telefono"],
            direccion=datos["direccion"],
            correo=correo,
            tienda_id=tienda.id,
        )

        await message.answer(
            f"✅ Cliente <b>{datos['nombre']}</b> creado correctamente."
        )

    finally:
        db.close()

    await state.clear()