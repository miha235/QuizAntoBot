import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import TOKEN
from handlers import start_game, check_answer

import logging

logging.basicConfig(level=logging.DEBUG)




print(f"TOKEN: {TOKEN}")  # Выведет токен (если пусто - проблема в загрузке .env)
bot = Bot(token=TOKEN)

dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("🏰The Grand Quest of Anto the Ant🇮🇹\n\n💌\"Per l'amore, niente è impossibile!\"\n\nDeep "
                         "in the Enchanted Garden of Lizard Wizard, where the cobblestone streets shimmer with ancient "
                         "magic and the wind carries whispers in Italian, Anto the Ant receives a mysterious message. "
                         "A tiny letter, sealed with a delicate imprint of a caterpillar, flutters into his hands.\n\n"
                         "\"Anto, my love, I am waiting for you at the top of the Great Fig Tree. But beware! The journey "
                         "is perilous, filled with trials that will test your wit, your memory, and your devotion. You "
                         "must travel through the enchanted realms, each one holding a challenge. Only if you solve all "
                         "the riddles and overcome every obstacle will you reach me. I believe in you, mio caro. \n\nAre you "
                         "ready for this adventure, my love? Yes or  No?\"")

# обработчик ошибок здесь
@dp.errors_handler()
async def error_handler(update, exception):
    logging.error(f"Update: {update} caused error: {exception}")
    return True  # Предотвращает повторное распространение ошибки


@dp.message()
async def handle_response(message: types.Message):
    user_id = message.from_user.id

    if message.text.lower() == "yes":
        await start_game(message)
    elif message.text.lower() == "no":
        await message.answer("💌 \"Oh, mio piccolo Anto… Do you truly wish to turn back? To let fate slip through your "
                             "tiny but mighty legs? I shall wait for you still, perched upon the Great Fig Tree, my "
                             "heart fluttering like the wind in the leaves. But every second without you is an eternity! "
                             "Perhaps, mio caro, you will find your courage and return when you are ready. I will be "
                             "waiting...\"\n\n🥀 The letter glows softly before fading into golden dust, as if giving "
                             "you one last chance to reconsider…")
    else:
        await check_answer(message)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
