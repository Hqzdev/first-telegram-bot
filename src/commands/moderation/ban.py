from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("ban"))
async def ban_user(message: Message, bot: Bot):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение!")
        return

    # Проверяем статус отправителя команды
    chat_member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if chat_member.status not in ["administrator", "creator"]:
        await message.reply("У тебя нет прав для выполнения этой команды.")
        return

    # Получаем ID пользователя, которого нужно забанить
    user_id_to_ban = message.reply_to_message.from_user.id

    # Блокируем пользователя
    await bot.ban_chat_member(chat_id=message.chat.id, user_id=user_id_to_ban)
    await message.reply(f"Пользователь **{message.reply_to_message.from_user.full_name}** был забанен.")

def register_ban_handlers(dp):
    dp.include_router(router)
