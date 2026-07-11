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
from handlers.productos.eliminar import router as productos_eliminar_router

# Clientes
from handlers.clientes.menu import router as clientes_menu_router
from handlers.clientes.crear import router as clientes_crear_router
from handlers.clientes.listar import router as cliente_listar_router
from handlers.clientes.editar import router as clientes_editar_router
from handlers.clientes.eliminar import router as clientes_eliminar_router
# Ventas
from handlers.ventas.menu import router as ventas_menu_router
from handlers.ventas.crear import router as ventas_crear_router
from handlers.ventas.listar import router as ventas_listar_router
from handlers.ventas.detalle import router as ventas_detalle_router
# Pagos
from handlers.pagos.menu import router as pagos_menu_router
from handlers.pagos.crear import router as pagos_crear_router
from handlers.pagos.listar import router as pagos_listar_router
# Reportes
from handlers.reportes.menu import router as reportes_menu_router
from handlers.reportes.dashboard import router as reportes_dashboard_router
from handlers.reportes.clientes_deuda import router as clientes_deuda_router
#Gastos
from handlers.gastos.menu import router as gastos_menu_router
from handlers.gastos.crear import router as gastos_crea_router
from handlers.gastos.listar import router as gastos_listar_router
# Caja
from handlers.caja.ver import router as caja_ver_router
# navegar
from handlers.navigation import router as navigation_router



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
dp.include_router(productos_eliminar_router)

# Clientes
dp.include_router(clientes_menu_router)
dp.include_router(clientes_crear_router)
dp.include_router(cliente_listar_router)
dp.include_router(clientes_editar_router)
dp.include_router(clientes_eliminar_router)

# Ventas
dp.include_router(ventas_menu_router)
dp.include_router(ventas_crear_router)
dp.include_router(ventas_listar_router)
dp.include_router(ventas_detalle_router)

#Pagos
dp.include_router(pagos_menu_router)
dp.include_router(pagos_crear_router)
dp.include_router(pagos_listar_router)


#reportes
dp.include_router(reportes_menu_router)
dp.include_router(reportes_dashboard_router)
dp.include_router(clientes_deuda_router)

#gastos
dp.include_router(gastos_menu_router)
dp.include_router(gastos_crea_router)
dp.include_router(gastos_listar_router)

# Caja
dp.include_router(caja_ver_router)
# Navegar
dp.include_router(navigation_router)




async def main():
    print("🤖 Bot iniciado correctamente...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())