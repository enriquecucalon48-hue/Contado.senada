from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_pagos = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💰 Registrar pago")],
        [KeyboardButton(text="📋 Ver pagos")],
        [KeyboardButton(text="⬅️ Menú principal")],
    ],
    resize_keyboard=True,
)