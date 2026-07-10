from aiogram.fsm.state import State, StatesGroup


class NuevaVenta(StatesGroup):
    cliente = State()
    producto = State()
    cantidad = State()
    carrito = State()
    confirmar = State()


class VerVenta(StatesGroup):
    seleccionar = State()