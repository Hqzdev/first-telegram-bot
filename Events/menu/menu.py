from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.filters import Command
from config import RAPIDAPI_KEY
import re
import aiohttp
import os
import logging
import json
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = Router()

# Создаем красивую клавиатуру с эмодзи
main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='ℹ️ Информация'),
            KeyboardButton(text='⚙️ Настройки')
        ],
        [
            KeyboardButton(text='🎮 Игры'),
            KeyboardButton(text='🎵 Музыка')
        ],
        [
            KeyboardButton(text='🌤 Погода'),
            KeyboardButton(text='📱 Поддержка')
        ],
        [
            KeyboardButton(text='🎲 Случайное число'),
            KeyboardButton(text='⏰ Время')
        ]
    ],
    resize_keyboard=True
)

# Обработчик команды /start
@router.message(Command("start"))
async def start_handler(message: Message):
    welcome_text = """
🌟 *Добро пожаловать!* 🌟

Я многофункциональный бот, который умеет:
• 📥 Скачивать видео из TikTok
• 🌤 Показывать погоду
• 🎮 Играть в мини-игры
• 🎵 Искать музыку
• ⚡️ И многое другое!

Используйте кнопки меню или следующие команды:
/help - список всех команд
/menu - открыть главное меню
/games - мини-игры
/weather - погода
/music - поиск музыки

*Отправьте мне ссылку на TikTok*, и я скачаю для вас видео!
    """
    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=main_menu_keyboard)

# Обработчик команды /help
@router.message(Command("help"))
async def help_handler(message: Message):
    help_text = """
📚 *Список доступных команд:*

*Основные команды:*
/start - 🚀 Перезапустить бота
/menu - 📱 Открыть главное меню
/help - 📖 Показать это сообщение

*Развлечения:*
/games - 🎮 Мини-игры
/random - 🎲 Случайное число
/music - 🎵 Поиск музыки

*Информация:*
/weather - 🌤 Узнать погоду
/time - ⏰ Текущее время
/info - ℹ️ Информация о боте

*Настройки и поддержка:*
/settings - ⚙️ Настройки бота
/support - 📱 Связаться с поддержкой

*Работа с TikTok:*
Просто отправьте мне ссылку на видео TikTok, и я скачаю его для вас! 📥
    """
    await message.answer(help_text, parse_mode="Markdown")

@router.message(Command("menu"))
async def show_menu(message: Message):
    await message.reply("📱 Выберите нужный раздел:", reply_markup=main_menu_keyboard)

# Обработчик для раздела Игры
@router.message(Command("games"))
async def games_handler(message: Message):
    games_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🎲 Кости", callback_data="game_dice"),
            InlineKeyboardButton(text="✂️ Камень-Ножницы-Бумага", callback_data="game_rps")
        ],
        [
            InlineKeyboardButton(text="🎯 Дартс", callback_data="game_darts"),
            InlineKeyboardButton(text="🎰 Слоты", callback_data="game_slots")
        ]
    ])
    await message.answer("🎮 Выберите игру:", reply_markup=games_keyboard)

# Обработчики игр
@router.callback_query(lambda call: call.data.startswith("game_"))
async def game_callback(call):
    game = call.data.split("_")[1]
    if game == "dice":
        await call.message.answer_dice(emoji="🎲")
    elif game == "darts":
        await call.message.answer_dice(emoji="🎯")
    elif game == "slots":
        await call.message.answer_dice(emoji="🎰")
    elif game == "rps":
        rps_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="✊ Камень", callback_data="rps_rock"),
                InlineKeyboardButton(text="✌️ Ножницы", callback_data="rps_scissors"),
                InlineKeyboardButton(text="✋ Бумага", callback_data="rps_paper")
            ]
        ])
        await call.message.answer("Выберите свой ход:", reply_markup=rps_keyboard)
    await call.answer()

# Обработчик времени
@router.message(Command("time"))
async def time_handler(message: Message):
    current_time = datetime.now().strftime("%H:%M:%S")
    await message.answer(f"⏰ Текущее время: {current_time}")

# Обработчик случайного числа
@router.message(Command("random"))
async def random_handler(message: Message):
    from random import randint
    number = randint(1, 100)
    await message.answer(f"🎲 Случайное число (1-100): *{number}*", parse_mode="Markdown")

# Обработчик информации
@router.message(Command("info"))
async def info_handler(message: Message):
    info_text = """
ℹ️ *Информация о боте*

🤖 Я многофункциональный бот-помощник, созданный для:
• Скачивания видео из TikTok
• Развлечений и мини-игр
• Получения полезной информации

📊 *Возможности:*
• Скачивание видео из TikTok
• Мини-игры и развлечения
• Информация о погоде
• Полезные утилиты

🔧 *Версия:* 1.0.0
👨‍💻 *Разработчик:* @your_username

Используйте /help для просмотра всех команд!
    """
    await message.answer(info_text, parse_mode="Markdown")

# Обработчик текстовых сообщений с кнопок
@router.message(F.text)
async def handle_text(message: Message):
    text = message.text.lower()
    
    if "информация" in text:
        await info_handler(message)
    elif "настройки" in text:
        await message.answer("⚙️ *Настройки бота*\n\nЗдесь будут настройки бота.", parse_mode="Markdown")
    elif "игры" in text:
        await games_handler(message)
    elif "музыка" in text:
        await message.answer("🎵 *Музыкальный раздел*\n\nФункция поиска музыки в разработке.", parse_mode="Markdown")
    elif "погода" in text:
        await weather_options(message)
    elif "поддержка" in text:
        await message.answer("📱 *Поддержка*\n\nЕсли у вас возникли вопросы, обратитесь к @your_username", parse_mode="Markdown")
    elif "случайное число" in text:
        await random_handler(message)
    elif "время" in text:
        await time_handler(message)
    else:
        # Проверяем, не является ли сообщение ссылкой на TikTok
        match = re.search(r'https?://[^/]*tiktok\.com/[^\s]+', message.text)
        if match:
            await process_tiktok_link(message)

async def process_tiktok_link(message: Message):
    await message.reply("⏳ Скачиваю видео из TikTok...")
    try:
        video_url = await get_tiktok_video_url(message.text)
        if video_url:
            filename = f"tiktok_{message.from_user.id}.mp4"
            await download_video(video_url, filename)
            video = FSInputFile(filename)
            await message.answer_video(video)
            os.remove(filename)
        else:
            await message.reply("❌ Не удалось получить видео по ссылке. Попробуйте другую ссылку.")
    except Exception as e:
        logger.error(f"Ошибка при скачивании: {str(e)}", exc_info=True)
        await message.reply(f"❌ Ошибка при скачивании: {str(e)}")

@router.message(lambda message: "Привет" in message.text.lower())
async def greet_user(message: Message):
    await message.reply("Привет! Чем могу помочь?")

@router.message(lambda message: "weather" in message.text.lower())
async def weather_options(message: Message):
    weather_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Moscow", callback_data="weather_moscow")],
        [InlineKeyboardButton(text="Saint Petersburg", callback_data="weather_spb")],
        [InlineKeyboardButton(text="Novosibirsk", callback_data="weather_novosibirsk")],
    ])
    await message.reply("Choose the city", reply_markup=weather_keyboard) 

@router.callback_query(lambda call: call.data.startswith("weather_"))
async def weather_callback(call):
    city = call.data.split("_")[1]
    city_names = {
        "moscow": "Moscow",
        "spb": "Saint Petersburg",
        "novosibirsk": "Novosibirsk"
    }
    selected_city = city_names.get(city, "Unknown city")
    await call.message.answer(f"Weather in {selected_city}: Weather forecast is not available yet.")
    await call.answer()

async def get_tiktok_video_url(tiktok_url):
    logger.debug(f"Запрос к API для получения видео: {tiktok_url}")
    
    # Преобразуем короткую ссылку в полную, если это vt.tiktok.com
    if 'vt.tiktok.com' in tiktok_url:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(tiktok_url, allow_redirects=True) as response:
                    tiktok_url = str(response.url)
                    logger.debug(f"Преобразованная ссылка: {tiktok_url}")
        except Exception as e:
            logger.error(f"Ошибка при преобразовании ссылки: {str(e)}")
    
    api = "https://tiktok-video-downloader-api.p.rapidapi.com/"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "tiktok-video-downloader-api.p.rapidapi.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            logger.debug(f"Отправка POST запроса к {api}")
            data = {"url": tiktok_url}
            async with session.post(api, json=data, headers=headers) as resp:
                logger.debug(f"Получен ответ от API. Статус: {resp.status}")
                logger.debug(f"Заголовки ответа: {resp.headers}")
                
                if resp.status == 200:
                    try:
                        data = await resp.json()
                        logger.debug(f"Ответ API: {data}")
                        
                        # Проверяем разные возможные пути к видео в ответе
                        if data.get("video"):
                            video_url = data["video"][0]
                            if video_url:
                                logger.info(f"Получена ссылка на видео: {video_url}")
                                return video_url
                        
                        if data.get("links"):
                            video_url = data["links"][0].get("link")
                            if video_url:
                                logger.info(f"Получена ссылка на видео из links: {video_url}")
                                return video_url
                                
                        if data.get("data"):
                            video_url = data["data"].get("play") or data["data"].get("video")
                            if video_url:
                                logger.info(f"Получена ссылка на видео из data: {video_url}")
                                return video_url
                        
                        logger.warning("В ответе API нет ссылки на видео")
                        logger.debug(f"Полный ответ API: {json.dumps(data, indent=2)}")
                        return None
                    except json.JSONDecodeError as e:
                        logger.error(f"Ошибка декодирования JSON: {str(e)}")
                        text_response = await resp.text()
                        logger.debug(f"Текст ответа: {text_response}")
                        return None
                else:
                    error_text = await resp.text()
                    logger.error(f"API вернул ошибку {resp.status}. Текст ошибки: {error_text}")
                    return None
    except Exception as e:
        logger.error(f"Ошибка при запросе к API: {str(e)}", exc_info=True)
        return None

async def download_video(url, filename):
    logger.debug(f"Начало загрузки видео: {url}")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    logger.debug("Получен ответ 200, сохраняем файл")
                    with open(filename, "wb") as f:
                        content = await resp.read()
                        f.write(content)
                    logger.info(f"Файл {filename} успешно сохранен")
                else:
                    logger.error(f"Ошибка при скачивании видео. Статус: {resp.status}")
                    raise Exception(f"Ошибка при скачивании видео. Статус: {resp.status}")
    except Exception as e:
        logger.error(f"Ошибка при скачивании видео: {str(e)}", exc_info=True)
        raise