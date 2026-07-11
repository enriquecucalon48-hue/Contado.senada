from aiogram.fsm.state import State, StatesGroup


class RegistrarPago(StatesGroup):
    venta = State()
    monto = State()