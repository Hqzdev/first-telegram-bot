from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

HELP_TEXT = """
📚 <b>Список всех доступных команд:</b>

💰 <b>Экономика:</b>
/balance - Проверить баланс
/work - Заработать монеты
/shop - Магазин предметов
/transfer - Перевести монеты другому пользователю
/top - Таблица лидеров по балансу

🎮 <b>Развлечения:</b>
/fact - Случайный интересный факт
/horoscope - Гороскоп (укажите знак зодиака)
/advice - Получить случайный совет
/joke - Случайная шутка
/compliment - Получить комплимент
/quote - Мотивационная цитата дня
/weather - Узнать текущую погоду
/random - Случайное число (можно указать диапазон)
/time - Текущее время
/calc - Калькулятор (например: /calc 2 + 2)

🛠 <b>Модерация:</b>
/ban - Забанить пользователя
/kick - Выгнать пользователя

ℹ️ <b>Прочее:</b>
/help - Показать это сообщение
/start - Начать работу с ботом

💡 <b>Совет:</b> Используйте /help чтобы в любой момент посмотреть список команд.
"""

@router.message(Command("help"))
async def show_help(message: Message):
    await message.reply(HELP_TEXT, parse_mode="HTML") 