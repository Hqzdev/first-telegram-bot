from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message(lambda message: message.text == "Information")
async def information_handler(message: Message):
    await message.answer("Information about the Yoku:\n\n I am a your personal assistant. I can help you with a lot of things. Just ask me what you need and I will try to help you.")  