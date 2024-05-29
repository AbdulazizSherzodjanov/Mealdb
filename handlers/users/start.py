from aiogram import types
import os
from keyboards.default import adminmenu
import sqlite3
from aiogram.dispatcher.filters.builtin import CommandStart
from data.config import ADMINS
from loader import dp, db, bot
from keyboards.default.usermenu import user_start


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    # Split the ADMINS string into a list and convert each element to an integer
    admin_ids = list(map(int, os.getenv('ADMINS').split(',')))

    if user_id in admin_ids:
        await message.answer("Hello Admin!", reply_markup=adminmenu.admin_start)
    else:
        name = message.from_user.full_name
        usern = message.from_user.username

        try:
            db.add_user(id=message.from_user.id,
                        name=name, username=usern)
        except sqlite3.IntegrityError as err:
            # await bot.send_message(chat_id=ADMINS[0],text=err)
            pass
            await message.answer(f"<i>Hello, {message.from_user.full_name} !</i>\n"
                                 "<i><b>Welcome to the bot.\nIn this bot,you can search and get random meals.</b></i>\n",
                                 parse_mode=types.ParseMode.HTML,reply_markup=user_start)
