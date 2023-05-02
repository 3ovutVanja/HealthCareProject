import asyncio
import config
import functools
from time import time
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(config.bot_token)
dp = Dispatcher(bot)
count = 0


def counter():
    global count
    count += 1


def my_decorator(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        print(time())
        result = await func(*args, **kwargs)
        return result
    return wrapper


async def my_func():
    while True:
        print(1)
        await asyncio.sleep(1)


async def on_startup(dp):
    asyncio.create_task(my_func())


@my_decorator
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    counter()
    await message.reply(text=config.HELP_COMMAND)


@my_decorator
@dp.message_handler(commands=['count'])
async def help_command(message: types.Message):
    global count
    counter()
    await message.answer(text=f'Сообщение номер {count}')


@my_decorator
@dp.message_handler(commands=['start'])
async def help_command(message: types.Message):
    await message.answer(text='добро пожаловать в бот')
    await message.delete()
    counter()


@my_decorator
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(text=message.text)
    counter()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

