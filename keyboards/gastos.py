from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_gastos = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Registrar gasto")],
        [KeyboardButton(text="📋 Ver gastos")],
        [KeyboardButton(text="⬅️ Volver")],
    ],
    resize_keyboard=True,
)

categorias_gastos = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📦 Inventario")],
        [KeyboardButton(text="🚚 Transporte")],
        [KeyboardButton(text="📢 Publicidad")],
        [KeyboardButton(text="🌐 Servicios")],
        [KeyboardButton(text="🍔 Alimentación")],
        [KeyboardButton(text="📁 Otros")],
    ],
    resize_keyboard=True,
)