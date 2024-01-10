from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.users import shop
from loader import dp
from utils.db_api.sqlite import insert_product
from states.states import AddproductState, AddRegistedState
from aiogram.dispatcher import FSMContext

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    check_user = await check(user_id=message.chat.id)
    if check_user is True:
        text ="botimizga "
    await message.answer(f"Salom, {message.from_user.full_name}!")
    await message.answer(reply_markup=shop)


@dp.message_handler(text="Mahsulot Qoshish ➕")
async def add_product_handler(message: types.Message, state: FSMContext):
    text = "Iltimos, mahsulot rasmini kiriting"
    await message.answer(text=text)
    await AddproductState.image.set()

@dp.message_handler(state=AddproductState.image, content_types=types.ContentType.PHOTO)
async def get_image_handler(message: types.Message, state: FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    text = "Iltimos mahsulot haqida ma'lumot kiriting."
    await message.answer(text=text)
    await AddproductState.info.set()


@dp.message_handler(state=AddproductState.info)
async def get_info_handler(message: types.Message, state: FSMContext):
    await state.update_data(info=message.text)
    text = "Iltimos mahsulot narxini kiriting."
    await message.answer(text=text)
    await AddproductState.price.set()



@dp.message_handler(state=AddproductState.price)
async def get_price_handler(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    text = "Iltimos mahsulot nomini kiriting."
    await message.answer(text=text)
    await AddproductState.name.set()



@dp.message_handler(state=AddproductState.name)
async def get_name_handler(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    text = "Iltimos aloqa uchun telefon raqam yoki telegram username kiriting."
    await message.answer(text=text)
    await AddproductState.contact.set()



@dp.message_handler(state=AddproductState.contact)
async def get_contact_handler(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text, chat_id=message.chat.id)
    data = await state.get_data()
    name = data.get('name')
    image = data.get('image')
    info = data.get('info')
    contact = data.get('contact')
    price = data.get('price')

    caption = f"Narxi: {name}\n{price}\n{info}\n\n{contact}"
    await message.answer_photo(photo=image, caption=caption )

    new_product = await insert_product(data=data)
    if new_product:
        text = "Mahsulot qo'shildi ✅"
    else:
        text = "Botda nosozlik bor"
    await message.answer(text=text, reply_markup=shop)
    await state.finish()


