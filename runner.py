
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '6562555378:AAHWj96HHAOeA2t6Vv8seiBXk02w7ylKZ5Y'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_lists = {}


@dp.message(Command('start'))
async def start(message: types.Message):
    user_id = message.from_user.id
    user_lists[user_id] = []
    buttons = [
        [KeyboardButton(text="Показать список")], [KeyboardButton(text="Удалить список")]
    ]
    markup = ReplyKeyboardMarkup(keyboard=buttons)
    await message.answer("Привет! Этот бот позволяет составлять, изменять и просматривать "
                         "список различных дел, в котором ты можешь планировать различные дела. "
                         "Для добавления нового пункта - просто напиши боту."
                         "Выбери действие:", reply_markup=markup)


@dp.message(lambda message: message.text == "Показать список")
async def show_list(message: types.Message):
    user_id = message.from_user.id
    todo_list = user_lists.get(user_id, [])
    if todo_list:
        items = "\n".join(f"{index + 1}. {item}" for index, item in enumerate(todo_list))
        buttons = [[InlineKeyboardButton(text="Удалить " + str(index + 1), callback_data="remove_" + str(index))]
                   for index in range(len(todo_list))]
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.answer(f"Твой список дел:\n{items}", reply_markup=markup)
    else:
        await message.answer("Твой список дел пуст.")


@dp.callback_query(lambda c: c.data.startswith('remove'))
async def remove_item_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    todo_list = user_lists.get(user_id, [])
    try:
        item_index = int(callback_query.data.split('_')[1])
        if 0 <= item_index < len(todo_list):
            removed_item = todo_list.pop(item_index)
            await bot.edit_message_text(f"Пункт '{removed_item}' удален из списка.", user_id,
                                        callback_query.message.message_id)
        else:
            await bot.answer_callback_query(callback_query.id, "Некорректный номер пункта.", show_alert=True)
    except (ValueError, IndexError):
        await bot.answer_callback_query(callback_query.id, "Произошла ошибка.", show_alert=True)


@dp.message(lambda message: message.text == "Удалить список")
async def delete_list(message: types.Message):
    user_id = message.from_user.id
    user_lists[user_id] = []
    await message.answer("Твой список дел был удален.")


@dp.message()
async def add_item_handler(message: types.Message):
    user_id = message.from_user.id
    new_item = message.text
    user_lists.setdefault(user_id, []).append(new_item)
    await message.answer(f"Добавлено в список: {new_item}")