from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
s = 0


@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью.")
    s = 1
    return s


if s == 0:
    @dp.message_handler()
    async def all_massages(message):
        await message.answer("Введите команду /start, чтобы начать общение.")


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text="Calories")
async def set_age(message):
    await message.answer("Введите свой возраст:")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(ag=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(grow=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weig=message.text)
    data = await state.get_data()
    norma = int(10 * int(data['weig']) + 6.25 * int(data['grow']) - 5 * int(data['ag']) + 5)
    await message.answer(f"Ваша норма в сутки {norma} ккал")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
