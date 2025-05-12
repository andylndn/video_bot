from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import os
import yt_dlp

# Получаем токен из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Создаём бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# /start команда
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer("👋 Привет! Отправь мне ссылку на видео, и я помогу тебе его скачать.")

# Обработка сообщений с ссылками
@dp.message()
async def handle_link(message: types.Message):
    url = message.text.strip()

    # Проверка, ссылка ли это
    if not url.startswith("http"):
        await message.answer("❌ Пожалуйста, отправь правильную ссылку на видео.")
        return

    await message.answer("⏬ Загружаю видео, подожди немного...")

    # Настройки загрузки видео
    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'mp4',
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # Отправляем видео пользователю
        with open(filename, 'rb') as video:
            await message.answer_video(video)

        # Удаляем файл после отправки
        os.remove(filename)

    except Exception as e:
        await message.answer(f"❌ Ошибка при загрузке видео: {e}")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

