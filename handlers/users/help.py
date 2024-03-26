from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Commands : ",
            "/start - Restart the bot",
            "/help - Help",
            "/random - Random recipe",
            "/search - Search meal")
    
    await message.answer("\n".join(text))
