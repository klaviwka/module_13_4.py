from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

API_TOKEN = ''

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Привет! Я бот, помогающий твоему здоровью.\nВведите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def ask_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.reply('Введите свой рост (в см):')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def ask_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.reply('Введите свой вес (в кг):')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def calculate_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)

    data = await state.get_data()
    age = int(data.get('age'))
    growth = float(data.get('growth'))
    weight = float(data.get('weight'))


    calories = 10 * weight + 6.25 * growth - 5 * age - 161

    await message.reply(f'Ваши калории: {calories:.2f}')

    await state.finish()


@dp.message_handler(lambda message: True)
async def fallback(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        await message.reply("Для начала работы с ботом введите /start")
    else:
        await message.reply("Пожалуйста, следуйте инструкциям и введите данные в нужном формате.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
