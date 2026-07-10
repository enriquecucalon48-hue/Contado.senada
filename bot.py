import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from handlers.start import router
from config import BOT_TOKEN
from handlers.tiendas.crear import router as tienda_router

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()
dp.include_router(router)
dp.include_router(tienda_router)
async def main():
    print("🤖 Bot iniciado correctamente...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())