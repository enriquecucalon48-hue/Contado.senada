from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

teclado_ventas = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Nueva venta")],
        [KeyboardButton(text="📋 Ver ventas")],
        [KeyboardButton(text="⬅️ Menú principal")],
    ],
    resize_keyboard=True,
)