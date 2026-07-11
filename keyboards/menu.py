from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_principal = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🏪 Tiendas")],
        [KeyboardButton(text="📦 Productos")],
        [KeyboardButton(text="👥 Clientes")],
        [KeyboardButton(text="🧾 Ventas")],
        [KeyboardButton(text="💵 Pagos")],
        [KeyboardButton(text="💸 Gastos")],
        [KeyboardButton(text="💰 Caja")],
        [KeyboardButton(text="📊 Reportes")],
        [KeyboardButton(text="🏠 Inicio")],
    ],
    resize_keyboard=True,
)