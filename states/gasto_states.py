from aiogram.fsm.state import State, StatesGroup


class RegistrarGasto(StatesGroup):
    concepto = State()
    categoria = State()
    monto = State()