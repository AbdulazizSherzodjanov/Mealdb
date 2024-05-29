from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_start= ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Foydanalunuvchilar soni"),
            KeyboardButton(text="Bazani yuklab olish"),
        ],
        [
            KeyboardButton(text="Reklama"),
            KeyboardButton(text="🔙Chiqish")
        ]
    ],
    resize_keyboard=True
)