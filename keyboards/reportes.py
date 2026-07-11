from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_reportes = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Dashboard")],
        [KeyboardButton(text="💳 Clientes con deuda")],
        [KeyboardButton(text="⬅️ Menú principal")],
    ],
    resize_keyboard=True,
)