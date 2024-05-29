from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
import requests
from loader import dp


@dp.message_handler(text="Random meal")
async def random_meal(message: types.Message):
    # Send request for getting responce
    responce = requests.get("https://www.themealdb.com/api/json/v1/1/random.php").json()

    # Get responce with for
    for i in responce["meals"]:
        name = i["strMeal"]
        category = i["strCategory"]
        area = i["strArea"]
        instruction = i["strInstructions"]
        youtube = i["strYoutube"]
        thumbnail = i["strMealThumb"]
    await message.answer(f"Sure! Here is a random recipe for you today! 😄\n\n"
                         f"<b>Name :</b> {name}\n\n"
                         f"<b>🖼 Image :</b> {thumbnail}\n\n"
                         f"<b>🔎Category :</b> {category}\n\n"
                         f"<b>🌎Area :</b> {area}\n\n"
                         f"<b>📃Instruction :</b> {instruction}\n\n"
                         f"<b>Youtube :</b> {youtube}\n", parse_mode=types.ParseMode.HTML)
