from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_principal = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🏪 Tiendas")],
        [KeyboardButton(text="📦 Productos")],
        [KeyboardButton(text="👥 Clientes")],
        [KeyboardButton(text="🧾 Ventas")],
        [KeyboardButton(text="💳 Deudas")],
        [KeyboardButton(text="💵 Pagos")],
        [KeyboardButton(text="📊 Reportes")],
    ],
    resize_keyboard=True,
)