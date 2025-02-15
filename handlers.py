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
        await message.answer ( "🎉 You've completed the quiz!" )
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
            await message.answer ( "\n\n😊 Добро Пожалуйста! You are right!" )
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
                    "❗ Ты ошибся 10 раз. Хочешь попробовать еще или показать правильный ответ? (Напиши 'еще' или 'ответ')" )

            else:
                await message.answer ( f"❌ Елки-Палки! Try again! (Attempts: {wrong_attempts[user_id]}/10)" )


async def handle_retry_or_answer(message: types.Message):
    """Обрабатывает выбор пользователя после 10 попыток."""
    user_id = message.from_user.id

    if user_id in current_question:
        index = current_question[user_id]
        correct_answer = QUESTIONS[index]["answer"]

        if message.text.strip ().lower () == "еще":
            awaiting_decision[user_id] = False  # Снимаем флаг ожидания
            await message.answer ( "💪 Try again!" )

        elif message.text.strip ().lower () == "ответ":
            await message.answer ( f"✅ Правильный ответ: {correct_answer}" )
            current_question[user_id] += 1  # Переход к следующему вопросу
            wrong_attempts[user_id] = 0  # Сброс ошибок
            awaiting_decision[user_id] = False  # Снимаем флаг ожидания
            await ask_question ( message,user_id )

        else:
            await message.answer ( "❗ Пожалуйста, напиши 'еще' или 'ответ'." )
