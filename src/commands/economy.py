from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import json
import os
import random
from datetime import datetime, timedelta

router = Router()
ECONOMY_FILE = "data/economy.json"

# Создаем папку data если её нет
os.makedirs("data", exist_ok=True)

# Загружаем или создаем экономику
def load_economy():
    if os.path.exists(ECONOMY_FILE):
        with open(ECONOMY_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_economy(data):
    with open(ECONOMY_FILE, 'w') as f:
        json.dump(data, f)

# Получить баланс пользователя
def get_balance(user_id):
    economy = load_economy()
    return economy.get(str(user_id), {"balance": 0, "last_work": None})

# Сохранить баланс пользователя
def save_balance(user_id, balance_data):
    economy = load_economy()
    economy[str(user_id)] = balance_data
    save_economy(economy)

@router.message(Command("balance"))
async def show_balance(message: Message):
    user_data = get_balance(message.from_user.id)
    balance = user_data["balance"]
    await message.reply(f"💰 Ваш баланс: {balance} монет")

@router.message(Command("work"))
async def work(message: Message):
    user_data = get_balance(message.from_user.id)
    last_work = user_data.get("last_work")
    
    if last_work:
        last_work = datetime.fromisoformat(last_work)
        if datetime.now() - last_work < timedelta(hours=1):
            remaining = timedelta(hours=1) - (datetime.now() - last_work)
            minutes = int(remaining.total_seconds() / 60)
            await message.reply(f"⏳ Вы сможете снова поработать через {minutes} минут!")
            return

    earnings = random.randint(10, 50)
    user_data["balance"] = user_data.get("balance", 0) + earnings
    user_data["last_work"] = datetime.now().isoformat()
    save_balance(message.from_user.id, user_data)
    
    await message.reply(f"💼 Вы поработали и заработали {earnings} монет!")

@router.message(Command("shop"))
async def shop(message: Message):
    shop_items = [
        {"name": "🎭 VIP статус", "price": 1000, "id": "vip"},
        {"name": "🎨 Кастомная роль", "price": 2000, "id": "custom_role"},
        {"name": "🎮 Игровой бустер", "price": 500, "id": "booster"}
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"{item['name']} - {item['price']} монет",
            callback_data=f"buy_{item['id']}"
        )] for item in shop_items
    ])
    
    await message.reply("🏪 Магазин:", reply_markup=keyboard)

@router.message(Command("transfer"))
async def transfer(message: Message):
    try:
        _, user_id, amount = message.text.split()
        amount = int(amount)
        
        if amount <= 0:
            await message.reply("❌ Сумма должна быть положительной!")
            return
            
        sender_data = get_balance(message.from_user.id)
        if sender_data["balance"] < amount:
            await message.reply("❌ У вас недостаточно монет!")
            return
            
        receiver_data = get_balance(int(user_id))
        
        sender_data["balance"] -= amount
        receiver_data["balance"] += amount
        
        save_balance(message.from_user.id, sender_data)
        save_balance(int(user_id), receiver_data)
        
        await message.reply(f"✅ Вы перевели {amount} монет пользователю!")
        
    except ValueError:
        await message.reply("❌ Используйте формат: /transfer <id> <сумма>")

@router.message(Command("top"))
async def show_top(message: Message):
    economy = load_economy()
    sorted_users = sorted(economy.items(), key=lambda x: x[1]["balance"], reverse=True)[:10]
    
    top_text = "🏆 Топ 10 богачей:\n\n"
    for i, (user_id, data) in enumerate(sorted_users, 1):
        top_text += f"{i}. ID: {user_id} - {data['balance']} монет\n"
    
    await message.reply(top_text)

@router.callback_query(lambda c: c.data.startswith('buy_'))
async def process_buy(callback_query):
    item_id = callback_query.data.split('_')[1]
    user_data = get_balance(callback_query.from_user.id)
    
    items = {
        "vip": {"price": 1000, "name": "VIP статус"},
        "custom_role": {"price": 2000, "name": "Кастомная роль"},
        "booster": {"price": 500, "name": "Игровой бустер"}
    }
    
    item = items.get(item_id)
    if not item:
        await callback_query.answer("❌ Предмет не найден!")
        return
        
    if user_data["balance"] < item["price"]:
        await callback_query.answer("❌ Недостаточно монет!")
        return
        
    user_data["balance"] -= item["price"]
    save_balance(callback_query.from_user.id, user_data)
    
    await callback_query.message.reply(f"✅ Вы купили {item['name']}!")
    await callback_query.answer() 