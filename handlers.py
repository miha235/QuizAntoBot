from aiogram import types
import json


# Загружаем вопросы из файла
def load_questions():
    with open ( "questions.json","r",encoding = "utf-8" ) as file:
        return json.load ( file )


QUESTIONS = load_questions ()

current_question = {}  # Текущий вопрос пользователя
wrong_attempts = {}  # Количество неверных попыток пользователя
awaiting_decision = {}  # Флаг, ждет ли бот ответа "еще" или "ответ"


async def start_game(message: types.Message):
    """Запускает игру и отправляет первый вопрос."""
    user_id = message.from_user.id
    current_question[user_id] = 0
    wrong_attempts[user_id] = 0  # Сбрасываем счетчик ошибок
    awaiting_decision[user_id] = False  # Сбрасываем флаг ожидания решения
    await ask_question ( message,user_id )


async def ask_question(message: types.Message,user_id: int):
    """Отправляет следующий вопрос."""
    if current_question[user_id] < len ( QUESTIONS ):
        question_text = QUESTIONS[current_question[user_id]]["question"]
        await message.answer ( question_text )
    else:
        await message.answer ( "🎉 🐜 Ant’s tiny legs tremble, not from exhaustion, but from anticipation. The Tower of "
                               "Echoes fades behind him as he ascends the final path—roots twisting like ancient stories"
                               " beneath his feet. Moonlight bathes the branches, and there, high above, stretches the "
                               "Fig Tree of Destiny, its leaves shimmering like emerald stars. \n\nPerched on a branch, "
                               "waiting with a smile brighter than the morning sun, is his beloved princess—the caterpillar "
                               "he longed for throughout his journey. Her eyes glisten with joy as Ant reaches her, the "
                               "weight of trials falling away like dew at dawn.\n\n🎉 Congratulations, brave traveler! "
                               "You’ve faced whispers, shadows, and timeless questions. You’ve carried the weight of "
                               "words and the burden of choice. And now—you’ve made it.\n\n🌿 But wait... there’s more! "
                               "Every true hero deserves a reward. Your journey has unlocked a special gift, crafted just "
                               "for you: \n\n🎁 Click here to receive your gift! \n"
                               "https://drive.google.com/drive/folders/1rE-rv89GjlrEzPNEmedRrvC6wlcHAT1I?usp=drive_link\n"
                               " \n\nThe princess giggles, her voice "
                               "like wind chimes swaying gently.\"You didn’t just walk a path,\" she says, \"you carved "
                               "one. And sometimes, the greatest treasures are not in the places you reach, but in the "
                               "journey that carries you there.\"\n\n🐜 Ant smiles, resting at last beneath the fig leaves, "
                               "the stars above whispering... \n\n\"Every ending holds the promise of a new beginning.\"")
        del current_question[user_id]
        del wrong_attempts[user_id]
        del awaiting_decision[user_id]


async def check_answer(message: types.Message):
    """Обрабатывает ответы пользователя."""
    user_id = message.from_user.id

    # Если ждем ответа "еще" или "ответ", перенаправляем обработку
    if awaiting_decision.get ( user_id,False ):
        await handle_retry_or_answer ( message )
        return

    if user_id in current_question:
        index = current_question[user_id]
        correct_answer = QUESTIONS[index]["answer"]

        if message.text.strip ().lower () == correct_answer.lower ():
            await message.answer ( "\n\n😊 Добро Пожалуйста! Welldone!" )
            current_question[user_id] += 1
            wrong_attempts[user_id] = 0  # Сбрасываем ошибки
            awaiting_decision[user_id] = False  # Сбрасываем флаг
            await ask_question ( message,user_id )
        else:
            wrong_attempts[user_id] += 1

            if wrong_attempts[user_id] == 5:
                hint = QUESTIONS[index]["hint"]
                await message.answer ( f"🤔 Hint: {hint}" )

            elif wrong_attempts[user_id] >= 10:
                awaiting_decision[user_id] = True  # Теперь бот ждет ответа пользователя
                await message.answer (
                    "\n❗Пердиндериндина!❗\n\nDo you want to keep suffering, or do you want me to show you the right answer? "
                    "(Choose 'suffering' or 'answer')" )

            else:
                await message.answer ( f"❌ Елки-Палки! Try again! (Attempts: {wrong_attempts[user_id]}/10)" )


async def handle_retry_or_answer(message: types.Message):
    """Обрабатывает выбор пользователя после 10 попыток."""
    user_id = message.from_user.id

    if user_id in current_question:
        index = current_question[user_id]
        correct_answer = QUESTIONS[index]["answer"]

        if message.text.strip ().lower () == "suffering":
            awaiting_decision[user_id] = False  # Снимаем флаг ожидания
            await message.answer ( "💪 Try again!" )

        elif message.text.strip ().lower () == "answer":
            await message.answer ( f"✅ The key: {correct_answer}" )
            current_question[user_id] += 1  # Переход к следующему вопросу
            wrong_attempts[user_id] = 0  # Сброс ошибок
            awaiting_decision[user_id] = False  # Снимаем флаг ожидания
            await ask_question ( message,user_id )

        else:
            await message.answer ( "❗ Please, write 'suffering' or 'answer'." )
