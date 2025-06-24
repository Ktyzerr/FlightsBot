from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
import asyncio
from aiogram.enums import ParseMode
import aiohttp
import requests

bot_token = '8135782654:AAFpCMOrrljABgrt3IqAP0nP65x0Lx9orFI'

bot = Bot(bot_token)
dp = Dispatcher()  

async def fetch_flights(origin, destination):
    url = 'https://api.travelpayouts.com/v2/prices/month-matrix'
    headers = {
    'X-Access-Token': '1596d4bae3c8d9059b4131f0b38f7761'
    }
    params = {
        'origin': origin,
        'destination': destination,
        'depart_date': '2025-03',
        'currency': 'rub',
        'one_way': 'true',
        'limit': 3  # топ 3 билета
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as resp:
            data = await resp.json()
            return data.get("data", [])

async def main():
    await dp.start_polling(bot)

@dp.message(F.text == "/start")
async def start(message:Message):
    await message.answer("Чтобы узнать какие еесть билеты напишите команду /check")

@dp.message(F.text == "/check")
async def check_flights(message:Message):
    await message.answer("🔍 Ищу дешёвые билеты на июнь...\n✈️ Москва/СПб → Таиланд")
    flights = []

    directions = [
        ('MOW', 'BKK'),  # Москва → Бангкок
        ('LED', 'BKK'),  # СПб → Бангкок
        ('MOW', 'HKT'),  # Москва → Пхукет
        ('LED', 'HKT')   # СПб → Пхукет
    ]

    for origin, dest in directions:
        data = await fetch_flights(origin, dest)
        for flight in data:
            price = flight.get('value')
            date = flight.get('depart_date')
            flights.append(f"{origin} → {dest}: <b>{price}₽</b> | 🗓 {date}")

    if flights:
        await message.answer("\n".join(flights), parse_mode="HTML")
    else:
        await message.answer("Билеты не найдены.")

if __name__ == "__main__":
    asyncio.run(main())
