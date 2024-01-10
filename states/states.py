from aiogram.dispatcher.filters.state import StatesGroup, State


class ContactState(StatesGroup):
    text = State()


class AddRegistedState(StatesGroup):
    name = State()
    phone_number = State()
    email = State()
    password = State()
    chat_id =State()

class AddproductState(StatesGroup):
    name = State()
    image = State()
    info = State()
    contact = State()
    price = State()