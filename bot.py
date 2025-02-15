import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import TOKEN
from handlers import start_game, check_answer

logging.basicConfig(level=logging.INFO)

if not TOKEN:
    raise ValueError("❌ TOKEN не найден! Проверь переменные среды.")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Are you ready to play ? (Reply with 'Yes' or 'No')")

@dp.message()
async def handle_response(message: types.Message):
    user_id = message.from_user.id

    if message.text.lower() == "yes":
        await start_game(message)
    elif message.text.lower() == "no":
        await message.answer("Alright, let me know when you are ready! 😊")
    else:
        await check_answer(message)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
