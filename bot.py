from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils import executor

API_TOKEN = '7971577062:AAG28HRJHktjxk9bdvUz5C00U0zf0nLYBz0'
ADMIN_ID = 580812971  # Замените на свой Telegram ID

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Сокращённый список направлений
directions = [
    "Соғлиқни сақлаш", "Таълим", "Транспорт", "Экология",
    "Маҳалла", "Коррупция", "Энергетика", "Тоза ичимлик суви",
    "Ёшлар сиёсати", "Қурилиш", "Ташқи иқтисод", "Бюджет",
    "Маданият", "Туризм", "Спорт", "Қишлоқ хўжалиги", "Солиқ",
    "Инвестиция", "Ижтимоий ҳимоя", "Жамоат транспорти",
    "Чиқинди",  "Ижро ҳокимият",  "Ички ишлар"
]

user_data = {}

def get_direction_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    buttons = [KeyboardButton(dir_name) for dir_name in directions]
    keyboard.add(*buttons)
    return keyboard

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # Удалим старую клавиатуру и покажем новую
    await message.answer("Клавиатура янгиланмоқда...", reply_markup=ReplyKeyboardRemove())
    await message.answer(
        "Ассалому алайкум!\n"
        "Сессияга тайёргарлик кўрилмоқда.\n"
        "Йўналишни танланг:",
        reply_markup=get_direction_keyboard()
    )

@dp.message_handler(lambda message: message.text in directions)
async def handle_direction(message: types.Message):
    user_data[message.from_user.id] = message.text
    await message.answer(f"Сиз '{message.text}'ни танладингиз. Илтимос, саволингизни ёзинг:")

@dp.message_handler(lambda message: message.from_user.id in user_data)
async def handle_question(message: types.Message):
    direction = user_data.pop(message.from_user.id)
    text = (
        f"📩 ЯНГИ САВОЛ\n"
        f"👤 @{message.from_user.username or message.from_user.full_name}\n"
        f"📌 Йўналиш: {direction}\n"
        f"❓ Савол: {message.text}"
    )
    await bot.send_message(chat_id=ADMIN_ID, text=text)
    await message.answer("Савол қабул қилинди! Рахмат. ✅")

if __name__ == '__main__':
    print("Бот запущен ✅")
    executor.start_polling(dp, skip_updates=True)
