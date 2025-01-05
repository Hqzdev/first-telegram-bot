from aiogram import types

async def start_command(message: types.Message):
    await message.reply("Привет! Я твой Telegram-бот, готов помочь!")

async def echo_message(message: types.Message):
    await message.answer(f"Ты написал: {message.text}")

def register_handlers(dp):
    dp.register_message_handler(start_command, commands=["start"])
    dp.register_message_handler(echo_message)
