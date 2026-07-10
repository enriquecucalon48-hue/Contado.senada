from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

teclado_clientes = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Nuevo cliente")],
        [KeyboardButton(text="📋 Ver clientes")],
        [KeyboardButton(text="✏️ Editar cliente")],
        [KeyboardButton(text="🗑 Eliminar cliente")],
        [KeyboardButton(text="⬅️ Menú principal")],
    ],
    resize_keyboard=True,
)