from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.conexion import SessionLocal
from database.repositories.usuario_repository import UsuarioRepository
from services.tienda_service import TiendaService
from states.tienda_states import CrearTienda

router = Router()


@router.message(F.text == "➕ Nueva tienda")
async def nueva_tienda(message: Message, state: FSMContext):
    await state.set_state(CrearTienda.nombre)

    await message.answer(
        "📝 Escribe el nombre de la tienda:"
    )


@router.message(CrearTienda.nombre)
async def recibir_nombre(message: Message, state: FSMContext):
    await state.update_data(nombre=message.text)

    await state.set_state(CrearTienda.direccion)

    await message.answer(
        "📍 Dirección (o escribe -):"
    )


@router.message(CrearTienda.direccion)
async def recibir_direccion(message: Message, state: FSMContext):
    direccion = None if message.text == "-" else message.text

    await state.update_data(direccion=direccion)

    await state.set_state(CrearTienda.telefono)

    await message.answer(
        "📞 Teléfono (o escribe -):"
    )


@router.message(CrearTienda.telefono)
async def recibir_telefono(message: Message, state: FSMContext):
    telefono = None if message.text == "-" else message.text

    await state.update_data(telefono=telefono)

    datos = await state.get_data()

    db = SessionLocal()

    try:
        usuario = UsuarioRepository.obtener_por_telegram_id(
            db,
            message.from_user.id,
        )

        if usuario is None:
            await message.answer("❌ Usuario no encontrado.")
            return

        TiendaService.crear(
            db=db,
            nombre=datos["nombre"],
            direccion=datos["direccion"],
            telefono=telefono,
            usuario_id=usuario.id,
        )

        await message.answer(
            f"✅ Tienda <b>{datos['nombre']}</b> creada correctamente."
        )

    finally:
        db.close()

    await state.clear()