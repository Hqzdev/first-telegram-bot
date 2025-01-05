from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message(lambda message: message.text == "Support")
async def information_handler(message: Message):
    await message.answer("**Support:**\n\n@Fucktheperson")  