from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.conexion import SessionLocal
from services.gasto_service import GastoService
from states.gasto_states import EliminarGasto

router = Router()


@router.message(F.text == "🗑 Eliminar gasto")
async def eliminar_gasto(
    message: Message,
    state: FSMContext,
):
    db = SessionLocal()

    try:
        gastos = GastoService.listar(db)

        if not gastos:
            await message.answer(
                "📭 No existen gastos registrados."
            )
            return

        texto = "🗑 Selecciona el gasto que deseas eliminar:\n\n"

        for i, gasto in enumerate(
            gastos,
            start=1,
        ):
            texto += (
                f"{i}. {gasto.concepto} "
                f"(${float(gasto.monto):.2f})\n"
            )

        await state.update_data(
            gastos=gastos,
        )

        await state.set_state(
            EliminarGasto.seleccionar,
        )

        await message.answer(texto)

    finally:
        db.close()


@router.message(EliminarGasto.seleccionar)
async def seleccionar_gasto(
    message: Message,
    state: FSMContext,
):
    datos = await state.get_data()

    gastos = datos["gastos"]

    try:
        indice = int(message.text) - 1
    except ValueError:
        await message.answer(
            "❌ Debes escribir un número."
        )
        return

    if indice < 0 or indice >= len(gastos):
        await message.answer(
            "❌ Ese gasto no existe."
        )
        return

    gasto = gastos[indice]

    await state.update_data(
        gasto_id=gasto.id,
    )

    await state.set_state(
        EliminarGasto.confirmar,
    )

    await message.answer(
        f"⚠️ ¿Eliminar el gasto '{gasto.concepto}'?\n\n"
        "Responde: SI o NO"
    )


@router.message(EliminarGasto.confirmar)
async def confirmar_eliminacion(
    message: Message,
    state: FSMContext,
):
    if message.text.upper() != "SI":
        await message.answer(
            "❌ Operación cancelada."
        )
        await state.clear()
        return

    datos = await state.get_data()

    db = SessionLocal()

    try:
        gasto = GastoService.obtener_por_id(
            db=db,
            gasto_id=datos["gasto_id"],
        )

        if gasto is None:
            await message.answer(
                "❌ Gasto no encontrado."
            )
            return

        GastoService.eliminar(
            db=db,
            gasto=gasto,
        )

        await message.answer(
            "✅ Gasto eliminado correctamente."
        )

    finally:
        db.close()

    await state.clear()