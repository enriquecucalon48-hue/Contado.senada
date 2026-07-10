from aiogram.fsm.state import State, StatesGroup


class CrearProducto(StatesGroup):
    nombre = State()
    precio = State()
    stock = State()


class EditarProducto(StatesGroup):
    seleccionar = State()
    precio = State()
    stock = State()

class EliminarProducto(StatesGroup):
    seleccionar = State()