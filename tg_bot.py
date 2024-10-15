import asyncio, requests, sqlite3, datetime, uvicorn
from aiogram import Bot, types, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from config import TOKEN, open_weather_api_token
from database import create_table
create_table()


bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command('weather'))
async def get_weather(message: Message, command: Command):
    if command.args is None:
        await message.answer('Введите название города! \n(Например, /weather Москва)')
    else:
        request = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={command.args}&units=metric&lang=ru&appid={open_weather_api_token}'
        )

        response = request.json()

        temp = response['main']['temp']
        temp_feels_like = response['main']['feels_like']
        weather = response['weather'][0]['description']
        humidity = response['main']['humidity']
        wind = response['wind']['speed']

    await message.answer(
        f'Температура: {temp}\n'
        f'Ощущается как: {temp_feels_like}\n'
        f'Погода: {weather}\n'
        f'Влажность: {humidity}\n'
        f'Скорость ветра: {wind}\n'
        )
    logs_db(message.from_user.id, message.text, f'Температура: {temp} Ощущается как: {temp_feels_like} Погода: {weather} Влажность: {humidity} Скорость ветра: {wind}')
    


def logs_db(user_id, command, response):
    conn = sqlite3.connect('bot_logs.db')
    cursor = conn.cursor()
    date_time = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    cursor.execute('''
                   INSERT INTO logs (user_id, command, date_time, response)
                   VALUES (?, ?, ?, ?)
                   ''', (user_id, command, date_time, response))
    conn.commit()
    conn.close()


async def main():
    await dp.start_polling(bot)
























if __name__ == '__main__':
    asyncio.run(main())