import logging

import django
import os
import sys

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()

import aiohttp
from aiogram.types import KeyboardButton
from aiogram import Dispatcher, types

from config_bot import BASE_URL, bot, WELCOME_TEXT

logging.basicConfig(level=logging.INFO)


storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class WeatherForecastState(StatesGroup):
    city_name = State()


@dp.message_handler(Text(equals="Главное меню"))
@dp.message_handler(commands=["/start", "старт", "start"])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton(text="Узнать погоду"))
    await message.answer(WELCOME_TEXT, reply_markup=keyboard)


@dp.message_handler(Text(equals="Узнать погоду"))
async def weather_forecast(message: types.Message, state: FSMContext):
    await message.answer('Конечно!\nТолько введите название города:')
    await state.set_state(WeatherForecastState.city_name.state)


@dp.message_handler(state=WeatherForecastState.city_name)
async def get_weather_forecast(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text="Главное меню"))

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}weather/?city={message.text}",) as resp:
            response = await resp.json()
    try:
        await message.answer(f"Погода в городе:{response['weather']['city_name']}:\n"
                             f"температура: {response['weather']['temperature']}°C;\n"
                             f"атмосферное давление: {response['weather']['pressure']} мм рт.ст.;\n"
                             f"скорость ветра: {response['weather']['wind_speed']} м/с", reply_markup=keyboard)
    except KeyError:
        await message.answer(f"{response['error']}.", reply_markup=keyboard)
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)