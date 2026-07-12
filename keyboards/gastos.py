from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_gastos = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Registrar gasto")],
        [KeyboardButton(text="📋 Ver gastos")],
        [KeyboardButton(text="🗑 Eliminar gasto")],
        [KeyboardButton(text="⬅️ Menú principal")],
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
        [KeyboardButton(text="⬅️ Menú principal")],
    ],
    resize_keyboard=True,
)