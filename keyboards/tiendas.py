from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_tiendas = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Nueva tienda")],
        [KeyboardButton(text="📋 Ver tiendas")],
        [KeyboardButton(text="⬅️ Menú principal")],
    ],
    resize_keyboard=True,
)