import os
import logging

from frontend.keyboard import maine_keyboard
from services.form import Form
from utils.configs import *
from frontend.messages import get_full_user_name, mess_about_create_event, message_event_name, message_description, \
    message_title, message_media, message_for_change_bot

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
# from aiogram.dispatcher.webhook import SendPhoto
from aiogram.types import ParseMode
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)


bot = Bot(token=os.environ["CLIENT_TOKEN"])

dp = Dispatcher(bot, )


@dp.message_handler(commands=['start'])
async def sent_welcome(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Добро пожаловать, {get_full_user_name(message)}",
                           reply_markup=maine_keyboard,
                           parse_mode='Markdown')


@dp.message_handler(content_types=types.ContentType.TEXT)
async def answer_main_buttons(message: types.Message):
    if message.text == "Добавить событие":
        await Form.event_name.set()

        await bot.send_message(message.chat.id, text=message_event_name)

        @dp.message_handler(state='*', commands='cancel')
        @dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
        async def cancel_handler(message: types.Message, state: FSMContext):

            current_state = await state.get_state()
            if current_state is None:
                return

            logging.info('Cancelling state %r', current_state)
            await state.finish()
            await bot.send_message(message.chat.id, text='Cancelled.', reply_markup=maine_keyboard)

        @dp.message_handler(state=Form.event_name)
        async def process_event_name(message: types.Message, state: FSMContext):

            async with state.proxy() as data:
                data['event_name'] = message.text

            await Form.next()
            await bot.send_message(message.chat.id, text=message_title)

        @dp.message_handler(state=Form.title)
        async def process_title(message: types.Message, state: FSMContext):

            async with state.proxy() as data:
                data['title'] = message.text

            await Form.next()
            await bot.send_message(message.chat.id, text=message_description)

        @dp.message_handler(state=Form.description)
        async def process_age(message: types.Message, state: FSMContext):

            async with state.proxy() as data:
                data['description'] = message.text

            await Form.next()

            await bot.send_message(message.chat.id, text=message_media)

        @dp.message_handler(content_types=['photo'], state=Form.media)
        async def process_media(message: types.Message, state: FSMContext):

            async with state.proxy() as data:
                await message.photo[-1].download(f'../media/{data["event_name"]}.jpg')

                data['media'] = f'{data["event_name"]}.jpg'
                data["end_time"] = None
                list_for_save_event.append(data)

                await bot.send_message(message.chat.id, text=mess_about_create_event(data),
                                       reply_markup=maine_keyboard,
                                       parse_mode=ParseMode.MARKDOWN)
                await bot.send_message(message.chat.id,
                                       text=message_for_change_bot)

            await state.finish()

    elif message.text == "Каталог":
        for i in range(len(list_for_save_event)):
            await bot.send_message(message.chat.id, text=mess_about_create_event(list_for_save_event[i]))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
