from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.conexion import SessionLocal
from keyboards.gastos import categorias_gastos
from services.gasto_service import GastoService
from states.gasto_states import RegistrarGasto

router = Router()


@router.message(F.text == "➕ Registrar gasto")
async def registrar_gasto(
    message: Message,
    state: FSMContext,
):
    await state.set_state(
        RegistrarGasto.concepto,
    )

    await message.answer(
        "📝 Escribe el concepto del gasto:"
    )


@router.message(RegistrarGasto.concepto)
async def guardar_concepto(
    message: Message,
    state: FSMContext,
):
    await state.update_data(
        concepto=message.text,
    )

    await state.set_state(
        RegistrarGasto.categoria,
    )

    await message.answer(
        "📂 Selecciona una categoría:",
        reply_markup=categorias_gastos,
    )


@router.message(RegistrarGasto.categoria)
async def guardar_categoria(
    message: Message,
    state: FSMContext,
):
    await state.update_data(
        categoria=message.text,
    )

    await state.set_state(
        RegistrarGasto.monto,
    )

    await message.answer(
        "💵 Escribe el monto del gasto:"
    )


@router.message(RegistrarGasto.monto)
async def guardar_gasto(
    message: Message,
    state: FSMContext,
):
    try:
        monto = float(message.text)
    except ValueError:
        await message.answer(
            "❌ Debes ingresar un número válido."
        )
        return

    datos = await state.get_data()

    db = SessionLocal()

    try:
        GastoService.crear(
            db=db,
            concepto=datos["concepto"],
            categoria=datos["categoria"],
            monto=monto,
        )

        await message.answer(
            "✅ Gasto registrado correctamente."
        )

    except ValueError as e:
        await message.answer(
            f"❌ {e}"
        )

    finally:
        db.close()

    await state.clear()