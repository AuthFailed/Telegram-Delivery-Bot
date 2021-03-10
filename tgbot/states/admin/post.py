from aiogram.dispatcher.filters.state import State, StatesGroup


class Post(StatesGroup):
    text = State()
    media = State()
    send = State()
