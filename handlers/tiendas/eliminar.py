from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.conexion import SessionLocal
from services.tienda_service import TiendaService
from states.tienda_states import EliminarTienda
from utils.contexto import obtener_usuario_actual

router = Router()


@router.message(F.text == "🗑 Eliminar tienda")
async def eliminar_tienda(
    message: Message,
    state: FSMContext,
):
    db = SessionLocal()

    try:
        usuario = obtener_usuario_actual(
            db,
            message,
        )

        if usuario is None:
            await message.answer(
                "❌ Usuario no encontrado."
            )
            return

        tiendas = TiendaService.listar(
            db=db,
            usuario_id=usuario.id,
        )

        if not tiendas:
            await message.answer(
                "🏪 No tienes tiendas registradas."
            )
            return

        texto = "🗑 Selecciona la tienda que deseas eliminar:\n\n"

        for i, tienda in enumerate(
            tiendas,
            start=1,
        ):
            texto += f"{i}. {tienda.nombre}\n"

        await state.update_data(
            tiendas=tiendas,
        )

        await state.set_state(
            EliminarTienda.seleccionar,
        )

        await message.answer(texto)

    finally:
        db.close()


@router.message(EliminarTienda.seleccionar)
async def seleccionar_tienda(
    message: Message,
    state: FSMContext,
):
    datos = await state.get_data()

    tiendas = datos["tiendas"]

    try:
        indice = int(message.text) - 1
    except ValueError:
        await message.answer(
            "❌ Debes escribir un número."
        )
        return

    if indice < 0 or indice >= len(tiendas):
        await message.answer(
            "❌ Esa tienda no existe."
        )
        return

    tienda = tiendas[indice]

    await state.update_data(
        tienda_id=tienda.id,
    )

    await state.set_state(
        EliminarTienda.confirmar,
    )

    await message.answer(
        f"⚠️ ¿Eliminar la tienda '{tienda.nombre}'?\n\n"
        "Responde: SI o NO"
    )


@router.message(EliminarTienda.confirmar)
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
        usuario = obtener_usuario_actual(
            db,
            message,
        )

        tiendas = TiendaService.listar(
            db=db,
            usuario_id=usuario.id,
        )

        tienda = next(
            (
                t for t in tiendas
                if t.id == datos["tienda_id"]
            ),
            None,
        )

        if tienda is None:
            await message.answer(
                "❌ Tienda no encontrada."
            )
            return

        TiendaService.eliminar(
            db=db,
            tienda=tienda,
        )

        await message.answer(
            "✅ Tienda eliminada correctamente."
        )

    finally:
        db.close()

    await state.clear()