from aiogram.fsm.state import State, StatesGroup


class RegistrarGasto(StatesGroup):
    concepto = State()
    categoria = State()
    monto = State()


class EliminarGasto(StatesGroup):
    seleccionar = State()
    confirmar = State()