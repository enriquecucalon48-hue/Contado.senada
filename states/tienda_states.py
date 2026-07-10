from aiogram.fsm.state import State, StatesGroup


class CrearTienda(StatesGroup):
    nombre = State()
    direccion = State()
    telefono = State()