from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
import requests
from states.search import RecipeSearch
from loader import dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command


@dp.message_handler(Command("cancel"), state=RecipeSearch.search)
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Search cancelled.")


@dp.message_handler(text="Search meal by name")
async def start_handler(message: types.Message):
    await message.answer("Please, send me name of meal which you want 😊\n"
                         "If you want to cancel, type /cancel command.")
    await RecipeSearch.search.set()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=RecipeSearch.search)
async def gpt(message: types.Message, state: FSMContext):
    user_search = message.text  # Get user's text
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={user_search}"  # Url variable with user's search
    url_without_quotes = url.replace("'", "")  # Remove any quotes
    responce = requests.get(url_without_quotes).json()
    # Get responce with for
    if responce is not None and "meals" in responce and isinstance(responce["meals"], list):
        for i in responce["meals"]:
            name = i["strMeal"]
            category = i["strCategory"]
            area = i["strArea"]
            instruction = i["strInstructions"]
            youtube = i["strYoutube"]
            thumbnail = i["strMealThumb"]
            ingredients_text = ""

            for meal in responce["meals"]:
                for number in range(1, 20):
                    ingredient_key = f"strIngredient{number}"
                    measure_key = f"strMeasure{number}"
                    ingredient_value = meal.get(ingredient_key)
                    measure_value = meal.get(measure_key)
                    if ingredient_value:
                        if measure_value:
                            ingredients_text += f"{measure_value} {ingredient_value}, "
                        else:
                            ingredients_text += f"{ingredient_value}, "

            ingredients_text = ingredients_text.rstrip(", ")
            search_reply = (f"Good\n"
                f"<b>Name :</b> {name}\n\n"
                f"<b>🖼 Image :</b><a href='{thumbnail}'> Click here</a>\n\n"
                f"<b>Category :</b> {category}\n\n"
                f"<b>Area :</b> {area}\n\n"
                f"<b>Instruction :</b> {instruction}\n\n"
                f"<b>Ingredients :</b> {ingredients_text}\n\n"
                f"<b>Youtube :</b> {youtube}\n"
            )
            max_length = 4096
            message_count = 0

            while search_reply and message_count < 5:
                    chunk = search_reply[:max_length]
                    search_reply = search_reply[max_length:]
                    await message.reply(chunk, parse_mode=types.ParseMode.HTML)
                    message_count += 1
                
            # After sending all chunks or reaching the message limit, provide the "cancel" instruction
            if message_count == 5:
                await message.reply("If you want to cancel, type /cancel command\.")
                break

        else:
            await message.reply("Sorry,no results found 😔.")
