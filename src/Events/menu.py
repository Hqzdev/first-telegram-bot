from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

router = Router()

main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        {KeyboardButton(text='Informaton')},
        {KeyboardButton(text='Settings')},
        {KeyboardButton(text='Support')}   
    ],
    resize_keyboard=True
)



@router.message(Command("menu"))
async def show_menu(message: Message):
    await message.reply("Choose the option you want", reply_markup=main_menu_keyboard)



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