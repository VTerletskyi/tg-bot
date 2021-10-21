from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    event_name = State()
    title = State()
    description = State()
    media = State()
    end_time = State()