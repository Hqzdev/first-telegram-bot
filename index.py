import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from config import BOT_TOKEN
from src.commands.moderation.ban import register_ban_handlers
from Events.menu.menu import router as menu_router
from Events.ready.commands_register import register_commands
from Events.menu.information import router as information_router
from Events.menu.settings import router as settings_router
from Events.menu.support import router as support_router

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

# Регистрация дополнительных обработчиков
dp.include_router(information_router)
dp.include_router(settings_router)
dp.include_router(support_router)
dp.include_router(menu_router)
register_ban_handlers(dp)

# Обработчик команды /start
@router.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer("Привет! Я готов помочь. Используй команды для взаимодействия.")

# Регистрация основного роутера
dp.include_router(router)

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
