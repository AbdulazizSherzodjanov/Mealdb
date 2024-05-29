from aiogram import types
import time
from data.config import ADMINS
from loader import db, dp, bot
from states.reklama import sendReklom
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from keyboards.default.usermenu import user_start

# Get all user
@dp.message_handler(text="Foydanalunuvchilar soni", user_id=ADMINS)
async def get_all_users(message: types.Message):
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    count_user = db.count_users()
    for i in count_user:
        await message.answer(f"{current_time} holatiga ko'ra foydalanuvchilar soni {i} ta")


# Cancelling advertisement
@dp.message_handler(Command("cancel_ad"), state=sendReklom.ad)
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Reklama bekor qilindi!")


@dp.message_handler(text="Reklama", user_id=ADMINS, state=None)
async def send_ad_to_all(message: types.Message, state: FSMContext):
    await message.answer("📢Reklama yuboring!\n"
                         "❗Agar reklamani bekor qilmoqchi bo'lsangiz /cancel_ad buyrug'ini yozing")
    await sendReklom.ad.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=sendReklom.ad)
async def send_ad(message: types.Message, state: FSMContext):
    await state.finish()
    users = db.select_all_users()
    user_count = db.count_users()
    for user in users:
        user_id = user[0]
        try:
            await bot.copy_message(chat_id=user_id, from_chat_id=message.chat.id,
                                   message_id=message.message_id, reply_markup=message.reply_markup,
                                   parse_mode=types.ParseMode.HTML)

            time.sleep(0.5)
        except Exception as e:
            print(e)
    await message.answer("✅ Reklama muvaffaqiyatli yuborildi!\n")
    await state.finish()


# Getting database file
@dp.message_handler(text="Bazani yuklab olish", user_id=ADMINS)
async def get_db(message: types.Message):
    file_path = open("data\main.db", 'rb')
    await message.answer_document(file_path)


# Exit for admin
@dp.message_handler(text="🔙Chiqish", user_id=ADMINS)
async def exit_admin(message: types.Message):
    await message.answer("Chiqildi",reply_markup=user_start)
