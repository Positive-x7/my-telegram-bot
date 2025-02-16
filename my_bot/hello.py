import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import openai
from dotenv import load_dotenv
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Загрузка переменных окружения
load_dotenv()

# Инициализация бота и диспетчера
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

# Инициализация OpenAI
openai.api_key = OPENAI_API_KEY

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот с искусственным интеллектом. Напиши мне что-нибудь, и я отвечу.")

# Обработчик всех сообщений
@dp.message_handler()
async def echo(message: types.Message):
    try:
        # Отправляем сообщение пользователя в OpenAI GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Используйте gpt-3.5-turbo или gpt-4
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message.text},
            ],
            max_tokens=150,
            temperature=0.7,
        )

        # Отправляем ответ пользователю
        if response.choices and response.choices[0].message.content:
            await message.answer(response.choices[0].message.content.strip())
        else:
            await message.answer("Произошла ошибка при обработке вашего запроса.")
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте позже.")

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)