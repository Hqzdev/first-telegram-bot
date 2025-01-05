from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message(lambda message: message.text == "Settings")
async def information_handler(message: Message):
    await message.answer("**Settings for Yoku:**\n\n Not available yet.")  