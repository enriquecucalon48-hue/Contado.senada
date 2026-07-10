from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.conexion import SessionLocal
from services.cliente_service import ClienteService
from states.cliente_states import EliminarCliente
from utils.contexto import (
    obtener_usuario_actual,
    obtener_tienda_actual,
)

router = Router()


@router.message(F.text == "🗑 Eliminar cliente")
async def eliminar_cliente(message: Message, state: FSMContext):
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

        texto = "🗑 Escribe el número del cliente que deseas eliminar.\n\n"

        for i, cliente in enumerate(clientes, start=1):
            texto += f"{i}. {cliente.nombre}\n"

        await state.update_data(clientes=clientes)

        await state.set_state(EliminarCliente.seleccionar)

        await message.answer(texto)

    finally:
        db.close()


@router.message(EliminarCliente.seleccionar)
async def confirmar_eliminacion(message: Message, state: FSMContext):
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

    db = SessionLocal()

    try:
        cliente_db = ClienteService.obtener_por_id(
            db=db,
            cliente_id=cliente.id,
        )

        if cliente_db is None:
            await message.answer("❌ Cliente no encontrado.")
            return

        ClienteService.eliminar(
            db=db,
            cliente=cliente_db,
        )

        await message.answer(
            f"🗑 Cliente <b>{cliente.nombre}</b> eliminado correctamente."
        )

    finally:
        db.close()

    await state.clear()