from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from services.pago_service import PagoService
from database.conexion import SessionLocal
from services.venta_service import VentaService
from states.pago_states import RegistrarPago
from utils.contexto import (
    obtener_usuario_actual,
    obtener_tienda_actual,
)

router = Router()


@router.message(F.text == "💰 Registrar pago")
async def registrar_pago(
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

        tienda = obtener_tienda_actual(
            db,
            usuario.id,
        )

        if tienda is None:
            await message.answer(
                "❌ No tienes una tienda creada."
            )
            return

        ventas = VentaService.listar(
            db=db,
            tienda_id=tienda.id,
        )

        if not ventas:
            await message.answer(
                "🧾 No existen ventas registradas."
            )
            return

        texto = "💰 Selecciona una venta:\n\n"

        for i, venta in enumerate(
            ventas,
            start=1,
        ):
            texto += (
                f"{i}. Venta #{venta.id} - "
                f"${venta.total}\n"
            )

        await state.update_data(
            ventas=ventas,
        )

        await state.set_state(
            RegistrarPago.venta,
        )

        await message.answer(texto)

    finally:
        db.close()

@router.message(RegistrarPago.venta)
async def seleccionar_venta(
    message: Message,
    state: FSMContext,
):
    datos = await state.get_data()

    ventas = datos["ventas"]

    try:
        indice = int(message.text) - 1
    except ValueError:
        await message.answer(
            "❌ Debes escribir un número."
        )
        return

    if indice < 0 or indice >= len(ventas):
        await message.answer(
            "❌ Esa venta no existe."
        )
        return

    venta = ventas[indice]

    await state.update_data(
        venta_id=venta.id,
    )

    await state.set_state(
        RegistrarPago.monto,
    )

    await message.answer(
        f"💰 Total de la venta: ${venta.total}\n\n"
        "Escribe el monto del pago:"
    )


@router.message(RegistrarPago.monto)
async def guardar_pago(
    message: Message,
    state: FSMContext,
):
    try:
        monto = float(message.text)
    except ValueError:
        await message.answer(
            "❌ Ingresa un monto válido."
        )
        return

    datos = await state.get_data()

    db = SessionLocal()

    try:
        PagoService.crear(
            db=db,
            venta_id=datos["venta_id"],
            monto=monto,
        )

        total_pagado = PagoService.total_pagado(
            db=db,
            venta_id=datos["venta_id"],
        )

        saldo = PagoService.saldo_pendiente(
            db=db,
            venta_id=datos["venta_id"],
        )

        venta = VentaService.obtener_por_id(
            db=db,
            venta_id=datos["venta_id"],
        )

        if saldo == 0:
            estado = "🟢 PAGADA"
        elif total_pagado == 0:
            estado = "🔴 PENDIENTE"
        else:
            estado = "🟡 PARCIAL"

        texto = (
            "✅ <b>Pago registrado correctamente</b>\n\n"
            f"🧾 Venta #{venta.id}\n"
            f"💰 Total: ${float(venta.total):.2f}\n"
            f"💵 Pagado: ${total_pagado:.2f}\n"
            f"💳 Saldo: ${saldo:.2f}\n"
            f"📌 Estado: {estado}"
        )

        await message.answer(texto)

    except ValueError as e:
        await message.answer(
            f"❌ {e}"
        )

    finally:
        db.close()

    await state.clear()