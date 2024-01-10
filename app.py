from aiogram import executor,types, Bot, Dispatcher, executor


from loader import dp
# import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from states.states import AddproductState, AddRegistedState
from aiogram.dispatcher import FSMContext
from states.insort.insort import insert_product
from keyboards.default.users import shop



async def on_startup(dispatcher):
    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)




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

# @dp.message_handler(text = "Registrasiya")
# async def get_Registrasiya_handler(message: types.Message):
#     text = "iltimos telefon raqamingizni kiriting"
#     await message.answer(text=text)
#     await AddRegistedState.phone_number.set()

# @dp.message_handler(state=AddRegistedState.phone_number)
# async def get_phone_number_handler(message: types.Message, state: FSMContext):
#     await state.update_data(phone_number=message.text)
#     text = "Iltimos emailingizni kiriting."
#     await message.answer(text=text)
#     await AddRegistedState.email.set()

# @dp.message_handler(state=AddRegistedState.email)
# async def get_email_handler(message: types.Message, state: FSMContext):
#     await state.update_data(email=message.text)
#     text = "Iltimos parolni kiriting."
#     await message.answer(text=text)
#     await AddRegistedState.password.set()


# @dp.message_handler(state=AddRegistedState.password)
# async def get_password_handler(message: types.Message, state: FSMContext):
#     await state.update_data(password=message.text)
#     data = await state.get_data()
#     phone_number = data.get("phone_number")
#     email = data.get("email")
#     password = data.get("password")
#     text ="registrasiadan otingiz"
#     await message.answer(text=text, reply_markup=shop)




#     caption = f"Register: {phone_number}\n{email}\n{password}"



if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
