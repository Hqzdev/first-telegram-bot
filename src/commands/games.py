from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import random

router = Router()

# Камень-ножницы-бумага
@router.message(Command("rps"))
async def rock_paper_scissors(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✊ Камень", callback_data="rps_rock"),
            InlineKeyboardButton(text="✌️ Ножницы", callback_data="rps_scissors"),
            InlineKeyboardButton(text="✋ Бумага", callback_data="rps_paper")
        ]
    ])
    await message.reply("Выберите свой ход:", reply_markup=keyboard)

@router.callback_query(lambda c: c.data.startswith('rps_'))
async def process_rps(callback_query):
    user_choice = callback_query.data.split('_')[1]
    choices = ['rock', 'paper', 'scissors']
    bot_choice = random.choice(choices)
    
    choice_emojis = {
        'rock': '✊',
        'paper': '✋',
        'scissors': '✌️'
    }
    
    result = ""
    if user_choice == bot_choice:
        result = "🤝 Ничья!"
    elif (
        (user_choice == 'rock' and bot_choice == 'scissors') or
        (user_choice == 'paper' and bot_choice == 'rock') or
        (user_choice == 'scissors' and bot_choice == 'paper')
    ):
        result = "🎉 Вы победили!"
    else:
        result = "😢 Вы проиграли!"
    
    await callback_query.message.edit_text(
        f"Ваш выбор: {choice_emojis[user_choice]}\n"
        f"Мой выбор: {choice_emojis[bot_choice]}\n\n"
        f"{result}"
    )

# Слоты
@router.message(Command("slots"))
async def slots(message: Message):
    emojis = ['🍎', '🍊', '🍇', '🍒', '🎰', '💎']
    result = [random.choice(emojis) for _ in range(3)]
    
    response = f"🎰 Слоты:\n\n{' | '.join(result)}\n\n"
    
    if len(set(result)) == 1:
        response += "🎉 ДЖЕКПОТ! Все символы совпали!"
    elif len(set(result)) == 2:
        response += "🎨 Неплохо! Есть совпадение!"
    else:
        response += "😢 Не повезло, попробуйте еще раз!"
    
    await message.reply(response)

# Кости
@router.message(Command("dice"))
async def dice(message: Message):
    await message.answer_dice(emoji="🎲")

# Дартс
@router.message(Command("darts"))
async def darts(message: Message):
    await message.answer_dice(emoji="🎯")

# Баскетбол
@router.message(Command("basketball"))
async def basketball(message: Message):
    await message.answer_dice(emoji="🏀")

# Футбол
@router.message(Command("football"))
async def football(message: Message):
    await message.answer_dice(emoji="⚽️")

# Казино
@router.message(Command("casino"))
async def casino(message: Message):
    await message.answer_dice(emoji="🎰")

# Угадай число
@router.message(Command("guess"))
async def guess_game(message: Message):
    number = random.randint(1, 100)
    await message.reply(
        "🎮 Я загадал число от 1 до 100!\n"
        "Используйте команду /number <число> для попытки угадать!"
    )
    
    # Сохраняем число для пользователя
    if not hasattr(router, "guess_numbers"):
        router.guess_numbers = {}
    router.guess_numbers[message.from_user.id] = number

@router.message(Command("number"))
async def check_number(message: Message):
    if not hasattr(router, "guess_numbers") or message.from_user.id not in router.guess_numbers:
        await message.reply("❌ Сначала начните игру командой /guess!")
        return
    
    try:
        guess = int(message.text.split()[1])
        number = router.guess_numbers[message.from_user.id]
        
        if guess == number:
            await message.reply("🎉 Поздравляю! Вы угадали число!")
            del router.guess_numbers[message.from_user.id]
        elif guess < number:
            await message.reply("⬆️ Мое число больше!")
        else:
            await message.reply("⬇️ Мое число меньше!")
    except (ValueError, IndexError):
        await message.reply("❌ Используйте формат: /number <число>")

# Виселица
WORDS = ['python', 'программирование', 'телеграм', 'бот', 'игра', 'команда']

@router.message(Command("hangman"))
async def hangman_game(message: Message):
    word = random.choice(WORDS)
    guessed = ['_'] * len(word)
    attempts = 6
    
    if not hasattr(router, "hangman_games"):
        router.hangman_games = {}
    
    router.hangman_games[message.from_user.id] = {
        'word': word,
        'guessed': guessed,
        'attempts': attempts,
        'used_letters': set()
    }
    
    await message.reply(
        f"🎮 Игра 'Виселица' начата!\n\n"
        f"Слово: {' '.join(guessed)}\n"
        f"Попыток осталось: {attempts}\n\n"
        f"Используйте /letter <буква> для отгадывания буквы!"
    )

@router.message(Command("letter"))
async def check_letter(message: Message):
    if not hasattr(router, "hangman_games") or message.from_user.id not in router.hangman_games:
        await message.reply("❌ Сначала начните игру командой /hangman!")
        return
    
    try:
        letter = message.text.split()[1].lower()
        game = router.hangman_games[message.from_user.id]
        
        if len(letter) != 1:
            await message.reply("❌ Введите только одну букву!")
            return
            
        if letter in game['used_letters']:
            await message.reply("❌ Эта буква уже была!")
            return
            
        game['used_letters'].add(letter)
        
        if letter in game['word']:
            for i, char in enumerate(game['word']):
                if char == letter:
                    game['guessed'][i] = letter
            
            if '_' not in game['guessed']:
                await message.reply(
                    f"🎉 Поздравляю! Вы отгадали слово: {game['word']}!"
                )
                del router.hangman_games[message.from_user.id]
                return
        else:
            game['attempts'] -= 1
            
        if game['attempts'] == 0:
            await message.reply(
                f"😢 Игра окончена! Слово было: {game['word']}"
            )
            del router.hangman_games[message.from_user.id]
            return
            
        await message.reply(
            f"Слово: {' '.join(game['guessed'])}\n"
            f"Попыток осталось: {game['attempts']}\n"
            f"Использованные буквы: {', '.join(sorted(game['used_letters']))}"
        )
        
    except IndexError:
        await message.reply("❌ Используйте формат: /letter <буква>") 