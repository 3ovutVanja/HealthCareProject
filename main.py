
import asyncio
import config
import functools
from time import time, sleep
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(config.bot_token)
dp = Dispatcher(bot)
count = 0


class Users:
    room = 1

    def __init__(self, id):
        self.id = id


list_of_activ_users = []
users = []


def my_decorator(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        print(time())
        user_id = args[0].from_user.id
        if user_id not in list_of_activ_users:
            list_of_activ_users.append(user_id)
            users.append(Users(user_id))
            user = users[-1]
        else:
            for user in users:
                if user.id == user_id:
                    break
        result = await func(*args, **kwargs)
        return result, user
    return wrapper


def counter():
    global count
    count += 1


async def my_func():
    g = time()
    while True:
        print(f'1 {time() - g}')
        g = time()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(my_func())


@dp.message_handler(commands=['count'])
async def help_command(message: types.Message):
    global count
    counter()
    await message.answer(text=f'Сообщение номер {count}')


@dp.message_handler()
@my_decorator
async def echo(message: types.Message):
    await message.answer(f'{message.text}')
    counter()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

