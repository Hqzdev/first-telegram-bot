import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from config import BOT_TOKEN
from src.commands import register_all_commands
from Events.menu.menu import router as menu_router
from Events.ready.commands_register import register_commands
from Events.menu.information import router as information_router
from Events.menu.settings import router as settings_router
from Events.menu.support import router as support_router

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Регистрация всех команд
register_all_commands(dp)

# Регистрация дополнительных обработчиков
dp.include_router(information_router)
dp.include_router(settings_router)
dp.include_router(support_router)
dp.include_router(menu_router)

# Основная функция запуска бота
async def main():
    try:
        # Регистрируем команды
        await register_commands(bot)
        # Запускаем polling
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Ошибка во время работы бота: {e}")

if __name__ == "__main__":
    asyncio.run(main())
