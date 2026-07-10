from aiogram.fsm.state import State, StatesGroup


class CrearCliente(StatesGroup):
    nombre = State()
    cedula = State()
    telefono = State()
    direccion = State()
    correo = State()


class EditarCliente(StatesGroup):
    seleccionar = State()
    nombre = State()
    cedula = State()
    telefono = State()
    direccion = State()
    correo = State()


class EliminarCliente(StatesGroup):
    seleccionar = State()