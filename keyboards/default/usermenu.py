from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_start= ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Random meal"),
            KeyboardButton(text="Search meal"),
        ],
    ],
    resize_keyboard=True
)