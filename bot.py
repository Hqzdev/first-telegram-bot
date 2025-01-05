import asyncio
import logging
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from config import BOT_TOKEN
from src.commands.ban import register_ban_handlers
from src.Events.menu import router as menu_router
from commands_register import register_commands

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

# Регистрация дополнительных обработчиков
dp.include_router(menu_router)
register_ban_handlers(dp)

# Обработчик команды /start
@router.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer("Hi, I'm Yoku, send /help to see the list of available commands")


# Регистрация основного роутера
dp.include_router(router)

# Основная функция запуска бота
async def main():
    logger.info("Бот запущен!")
    try:
        # Регистрируем команды
        await register_commands(bot)
        # Запускаем polling
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(f"Ошибка во время работы бота: {e}")

if __name__ == "__main__":
    asyncio.run(main())
