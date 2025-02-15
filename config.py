from dotenv import load_dotenv
import os

load_dotenv()  # Загружаем переменные из .env

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN не загружен! Проверь .env файл или переменные окружения.")


DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")
