import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN

# Routers
from handlers.start import router as start_router

# Tiendas
from handlers.tiendas.menu import router as tiendas_menu_router
from handlers.tiendas.crear import router as tiendas_crear_router

# Productos
from handlers.productos.menu import router as productos_menu_router
from handlers.productos.crear import router as productos_crear_router
from handlers.productos.listar import router as productos_listar_router
from handlers.productos.editar import router as productos_editar_router
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
    ),
)

dp = Dispatcher()

# ==========================
# Routers
# ==========================

dp.include_router(start_router)

# Tiendas
dp.include_router(tiendas_menu_router)
dp.include_router(tiendas_crear_router)

# Productos
dp.include_router(productos_menu_router)
dp.include_router(productos_crear_router)
dp.include_router(productos_listar_router)
dp.include_router(productos_editar_router)
async def main():
    print("🤖 Bot iniciado correctamente...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())