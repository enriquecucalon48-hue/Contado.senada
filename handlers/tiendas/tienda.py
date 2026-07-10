from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states.tienda_states import CrearTienda

router = Router()


@router.message(F.text == "🏪 Tiendas")
async def crear_tienda(message: Message, state: FSMContext):
    await state.set_state(CrearTienda.nombre)

    await message.answer(
        "🏪 Vamos a crear tu primera tienda.\n\n"
        "✍️ Escribe el nombre de la tienda:"
    )


@router.message(CrearTienda.nombre)
async def recibir_nombre(message: Message, state: FSMContext):
    await state.update_data(nombre=message.text)


    await state.set_state(CrearTienda.direccion)


    await message.answer(
        "📍 Escribe la dirección de la tienda.\n\n"
        "Si no deseas agregar una dirección, escribe -"

    )

@router.message(CrearTienda.direccion)
async def recibir_direccion(message: Message, state: FSMContext):
    direccion = None if message.text == "-" else message.text

    await state.update_data(direccion=direccion)

    await state.set_state(CrearTienda.telefono)

    await message.answer(
        "📞 Escribe el teléfono.\n\n"
        "Si no deseas agregar uno, escribe -"

    )

@router.message(CrearTienda.telefono)
async def recibir_telefono(message: Message, state: FSMContext):
    telefono = None if message.text == "-" else message.text

    await state.update_data(telefono=telefono)

    datos = await state.get_data()

    await message.answer(
        f"""
✅ Datos recibidos

🏪 Nombre: {datos['nombre']}
📍 Dirección: {datos['direccion']}
📞 Teléfono: {telefono}
"""
    )

    await state.clear()