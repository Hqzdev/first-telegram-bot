from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
import random
import datetime

router = Router()

# Случайные факты
FACTS = [
    "🌍 Земля — единственная планета, названная не в честь бога.",
    "🦒 Жирафы могут чистить свои уши языком.",
    "🧠 Мозг на 80% состоит из воды.",
    "🌈 Радуга на самом деле круглая, мы видим только её часть.",
    "🦈 Акулы существовали раньше, чем деревья.",
    "🌙 На Луне есть следы 12 человек.",
    "🐜 Муравьи никогда не спят.",
    "🦋 Бабочки чувствуют вкус лапками.",
    "🐘 Слоны — единственные животные, которые не могут прыгать.",
    "🌞 Свет от Солнца достигает Земли за 8 минут."
]

@router.message(Command("fact"))
async def random_fact(message: Message):
    fact = random.choice(FACTS)
    await message.reply(fact)

# Гороскоп
ZODIAC_SIGNS = {
    "овен": "♈️",
    "телец": "♉️",
    "близнецы": "♊️",
    "рак": "♋️",
    "лев": "♌️",
    "дева": "♍️",
    "весы": "♎️",
    "скорпион": "♏️",
    "стрелец": "♐️",
    "козерог": "♑️",
    "водолей": "♒️",
    "рыбы": "♓️"
}

PREDICTIONS = [
    "Сегодня отличный день для новых начинаний!",
    "Будьте осторожны в финансовых вопросах.",
    "Вас ждет приятный сюрприз.",
    "Хороший день для общения и новых знакомств.",
    "Возможны неожиданные перемены.",
    "Прекрасное время для творчества.",
    "Уделите внимание здоровью.",
    "Вас ждет успех в любовных делах.",
    "Благоприятный день для работы и учебы.",
    "Проведите время с семьей."
]

@router.message(Command("horoscope"))
async def horoscope(message: Message):
    try:
        sign = message.text.split()[1].lower()
        if sign in ZODIAC_SIGNS:
            prediction = random.choice(PREDICTIONS)
            emoji = ZODIAC_SIGNS[sign]
            await message.reply(f"{emoji} Гороскоп для {sign.capitalize()}:\n\n{prediction}")
        else:
            signs_list = "\n".join([f"{v} {k.capitalize()}" for k, v in ZODIAC_SIGNS.items()])
            await message.reply(f"❌ Укажите ваш знак зодиака:\n\n{signs_list}")
    except IndexError:
        signs_list = "\n".join([f"{v} {k.capitalize()}" for k, v in ZODIAC_SIGNS.items()])
        await message.reply(f"❌ Используйте формат: /horoscope <знак>\n\nДоступные знаки:\n{signs_list}")

# Случайный совет
ADVICE = [
    "💡 Начните день с улыбки!",
    "🎯 Поставьте себе новую цель.",
    "📚 Прочитайте новую книгу.",
    "🏃 Займитесь спортом.",
    "🎨 Попробуйте что-то новое.",
    "💪 Не сдавайтесь, у вас всё получится!",
    "🌟 Верьте в себя.",
    "🤝 Помогите кому-нибудь сегодня.",
    "🧘 Найдите время для медитации.",
    "✍️ Запишите свои мысли в дневник."
]

@router.message(Command("advice"))
async def random_advice(message: Message):
    advice = random.choice(ADVICE)
    await message.reply(advice)

# Случайная шутка
JOKES = [
    "😄 Почему программисты путают Хэллоуин и Рождество? Потому что 31 OCT = 25 DEC",
    "😅 Какой самый любимый напиток программиста? Java!",
    "😂 Что сказал HTML CSS? Ты такой стильный!",
    "🤣 Почему Python не носит очки? Потому что он не С Sharp!",
    "😆 Как программист ботаник называет свой сад? Массив цветов!",
    "😄 Что сказал один байт другому байту? Встретимся в порту!",
    "😅 Почему компьютер устал? Потому что у него была тяжелая база данных!",
    "😂 Что сказал сервер клиенту? Ответ: 200 ОК!",
    "🤣 Как называется группа из 8 бит, которые собираются вместе? Байтовая банда!",
    "😆 Что общего между программистом и поэтом? Оба используют строки!"
]

@router.message(Command("joke"))
async def random_joke(message: Message):
    joke = random.choice(JOKES)
    await message.reply(joke)

# Комплимент
COMPLIMENTS = [
    "✨ Вы сегодня великолепно выглядите!",
    "🌟 У вас замечательная улыбка!",
    "💫 Вы очень талантливы!",
    "🌈 С вами так приятно общаться!",
    "💝 Вы делаете мир лучше!",
    "🎯 У вас отличное чувство юмора!",
    "🌺 Вы источник вдохновения для других!",
    "💫 Ваша энергия заряжает позитивом!",
    "🌟 Вы умеете находить подход к людям!",
    "✨ Вы невероятно умны и проницательны!"
]

@router.message(Command("compliment"))
async def send_compliment(message: Message):
    compliment = random.choice(COMPLIMENTS)
    await message.reply(compliment)

# Цитата дня
QUOTES = [
    "💭 «Единственный способ делать великие дела — любить то, что вы делаете» - Стив Джобс",
    "💫 «Будьте изменениями, которые вы хотите видеть в мире» - Махатма Ганди",
    "🌟 «Жизнь — это то, что с вами происходит, пока вы строите планы» - Джон Леннон",
    "✨ «Успех — это способность идти от неудачи к неудаче, не теряя энтузиазма» - Уинстон Черчилль",
    "💫 «Лучший способ предсказать будущее — создать его» - Питер Друкер",
    "🌠 «Если вы можете мечтать об этом, вы можете это сделать» - Уолт Дисней",
    "💭 «Жизнь либо отважное приключение, либо ничего» - Хелен Келлер",
    "✨ «Каждый день — это новый шанс изменить свою жизнь» - Unknown",
    "🌟 «Никогда не поздно быть тем, кем вы могли бы быть» - Джордж Элиот",
    "💫 «Ваше время ограничено, не тратьте его, живя чужой жизнью» - Стив Джобс"
]

@router.message(Command("quote"))
async def daily_quote(message: Message):
    quote = random.choice(QUOTES)
    await message.reply(quote)

# Погода (имитация)
WEATHER_CONDITIONS = [
    "☀️ Солнечно",
    "🌤 Переменная облачность",
    "☁️ Облачно",
    "🌧 Дождь",
    "⛈ Гроза",
    "❄️ Снег",
    "🌫 Туман"
]

@router.message(Command("weather"))
async def weather_forecast(message: Message):
    condition = random.choice(WEATHER_CONDITIONS)
    temp = random.randint(-10, 30)
    humidity = random.randint(30, 90)
    wind = random.randint(0, 20)
    
    forecast = f"""
🌡 Погода сейчас:
{condition}
Температура: {temp}°C
Влажность: {humidity}%
Ветер: {wind} м/с
    """
    await message.reply(forecast)

# Случайное число
@router.message(Command("random"))
async def random_number(message: Message):
    try:
        args = message.text.split()[1:]
        if len(args) == 2:
            start, end = map(int, args)
            number = random.randint(start, end)
            await message.reply(f"🎲 Случайное число от {start} до {end}: {number}")
        else:
            number = random.randint(1, 100)
            await message.reply(f"🎲 Случайное число (1-100): {number}")
    except:
        await message.reply("❌ Используйте формат: /random [начало] [конец]")

# Время
@router.message(Command("time"))
async def current_time(message: Message):
    now = datetime.datetime.now()
    await message.reply(f"⏰ Текущее время: {now.strftime('%H:%M:%S')}")

# Калькулятор
@router.message(Command("calc"))
async def calculator(message: Message):
    try:
        expression = " ".join(message.text.split()[1:])
        if not expression:
            raise ValueError
            
        # Безопасное выполнение выражения
        allowed_chars = set("0123456789+-*/() ")
        if not all(c in allowed_chars for c in expression):
            raise ValueError
            
        result = eval(expression)
        await message.reply(f"🔢 {expression} = {result}")
    except:
        await message.reply("❌ Используйте формат: /calc <выражение>\nПример: /calc 2 + 2 * 2") 