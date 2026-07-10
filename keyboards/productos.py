from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

teclado_productos = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Nuevo producto")],
        [KeyboardButton(text="📋 Ver productos")],
        [KeyboardButton(text="✏️ Editar producto")],
        [KeyboardButton(text="🗑 Eliminar producto")],
        [KeyboardButton(text="⬅️ Menú principal")],
    ],
    resize_keyboard=True,
)