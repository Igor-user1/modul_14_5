from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from crud_functions import *

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text="Рассчитать")
button2 = KeyboardButton(text="Информация")
button3 = KeyboardButton(text="Купить")
button4 = KeyboardButton(text='Регистрация')
kb.add(button, button2, button3, button4)


kb1 = InlineKeyboardMarkup(resize_keyboard=True)
inline_bottom = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
inline_bottom2 = InlineKeyboardButton(text='Формулы расчета', callback_data='formulas')
kb1.add(inline_bottom, inline_bottom2)

kb2 = InlineKeyboardMarkup(resixe_keyboard=True)
inline_buy_bottom1 = InlineKeyboardButton(text='Банан', callback_data='product_buying')
inline_buy_bottom2 = InlineKeyboardButton(text='Яблоко', callback_data='product_buying')
inline_buy_bottom3 = InlineKeyboardButton(text='Абрикос', callback_data='product_buying')
inline_buy_bottom4 = InlineKeyboardButton(text='Виноград', callback_data='product_buying')
kb2.add(inline_buy_bottom1, inline_buy_bottom2, inline_buy_bottom3, inline_buy_bottom4)

@dp.message_handler(text=["Рассчитать"])
async def main_menu(message):
    await message.answer('Выберите опцию: ', reply_markup=kb1)

@dp.message_handler(text=["Купить"])
async def get_buying_list(message):
    for i in range(4):
        with open(f'{i + 1}.jpeg', 'rb') as img:
            await message.answer_photo(img, f'Название: {get_all_products()[i][1]} |'
                                            f' Описание: {get_all_products()[i][2]} |'
                                            f' Цена: {get_all_products()[i][3]}')
    await message.answer("Выберите продукт для покупки:", reply_markup=kb2)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')

@dp.message_handler(text=['/start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.callback_query_handler(text=['formulas'])
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х'
                      'возраст (г) + 5')
    await call.answer()


@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(first=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(second=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(third=message.text)
    data = await state.get_data()
    await message.answer(f'Ваша норма калорий '
                         f'{int(data["third"])*10 + int(data["second"])*6.25 - int(data["first"])*5 + 5}')
    await state.finish()


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text) is False:
        await state.update_data(first=message.text)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()
    else:
        await message.answer('Пользователь существует, введите другое имя')
        await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(second=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(third=message.text)
    data = await state.get_data()
    add_user(data['first'], data['second'], data['third'])
    await message.answer("Регистрация прошла успешно")
    await state.finish()

@dp.message_handler()
async def all_messages(message):
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)