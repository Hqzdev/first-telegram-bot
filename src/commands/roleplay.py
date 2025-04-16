from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
import random

router = Router()

# Ролевые действия
ACTIONS = {
    "hug": ["обнял", "обняла", "🤗"],
    "kiss": ["поцеловал", "поцеловала", "💋"],
    "pat": ["погладил", "погладила", "🤚"],
    "bite": ["укусил", "укусила", "😈"],
    "slap": ["ударил", "ударила", "👋"],
    "kill": ["убил", "убила", "💀"],
    "love": ["признался в любви к", "призналась в любви к", "❤️"],
    "marry": ["женился на", "вышла замуж за", "💍"],
    "dance": ["танцует с", "танцует с", "💃"],
    "cry": ["плачет из-за", "плачет из-за", "😢"],
    "laugh": ["смеётся над", "смеётся над", "😂"],
    "poke": ["тыкает", "тыкает", "👉"],
    "wave": ["машет", "машет", "👋"],
    "highfive": ["дал пять", "дала пять", "🖐"],
    "handshake": ["пожал руку", "пожала руку", "🤝"],
    "bow": ["поклонился", "поклонилась", "🙇"],
    "wink": ["подмигнул", "подмигнула", "😉"],
    "sleep": ["спит рядом с", "спит рядом с", "😴"],
    "punch": ["ударил", "ударила", "👊"],
    "feed": ["покормил", "покормила", "🍽"]
}

# Генератор сообщений для действий
def generate_action_message(action, user_name, target_name, gender="male"):
    if action not in ACTIONS:
        return None
    
    verb, _, emoji = ACTIONS[action]
    if gender == "female":
        verb = ACTIONS[action][1]
    
    messages = [
        f"{emoji} | {user_name} {verb} {target_name}",
        f"{emoji} | {user_name} нежно {verb} {target_name}",
        f"{emoji} | {user_name} мило {verb} {target_name}",
        f"{emoji} | {user_name} неожиданно {verb} {target_name}",
        f"{emoji} | {user_name} страстно {verb} {target_name}"
    ]
    return random.choice(messages)

# Создаем обработчики для каждого действия
for action in ACTIONS.keys():
    @router.message(Command(action))
    async def handle_action(message: Message):
        command = message.text.split()[0][1:]  # Получаем команду без /
        try:
            target = " ".join(message.text.split()[1:])
            if not target:
                await message.reply(f"❌ Используйте формат: /{command} <имя>")
                return
                
            user_name = message.from_user.first_name
            # Определяем пол по имени (простая реализация)
            gender = "female" if user_name.lower().endswith(('а', 'я')) else "male"
            
            action_message = generate_action_message(command, user_name, target, gender)
            if action_message:
                await message.reply(action_message)
            
        except Exception as e:
            await message.reply(f"❌ Используйте формат: /{command} <имя>")

# Специальные команды
@router.message(Command("me"))
async def me_action(message: Message):
    try:
        action = " ".join(message.text.split()[1:])
        if not action:
            await message.reply("❌ Используйте формат: /me <действие>")
            return
            
        user_name = message.from_user.first_name
        await message.reply(f"🎭 | {user_name} {action}")
    except:
        await message.reply("❌ Используйте формат: /me <действие>")

@router.message(Command("do"))
async def do_action(message: Message):
    try:
        action = " ".join(message.text.split()[1:])
        if not action:
            await message.reply("❌ Используйте формат: /do <действие>")
            return
            
        await message.reply(f"🎭 | {action}")
    except:
        await message.reply("❌ Используйте формат: /do <действие>") 