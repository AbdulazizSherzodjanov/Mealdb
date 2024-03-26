from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
import requests
from states.search import RecipeSearch
from loader import dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command


@dp.message_handler(Command("cancel"), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()  # Reset user state
    await message.reply("Search cancelled.")


@dp.message_handler(commands=['search'])
async def start_handler(message: types.Message):
    await message.answer("Please, send me name of meal which you want 😊")
    await RecipeSearch.search.set()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=RecipeSearch.search)
async def gpt(message: types.Message, state: FSMContext):
    user_search = message.text  # Get user's text
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={user_search}"  # Url variable with user's search
    url_without_quotes = url.replace("'", "")  # Remove any quotes
    responce = requests.get(url_without_quotes).json()  # Get response
    # Get responce with for
    if responce is not None and "meals" in responce and isinstance(responce["meals"], list):
        for i in responce["meals"]:
            name = i["strMeal"]
            category = i["strCategory"]
            area = i["strArea"]
            instruction = i["strInstructions"]
            youtube = i["strYoutube"]
            thumbnail = i["strMealThumb"]
            ingredients_text = ""  # Initialize an empty string to store ingredients

            for meal in responce["meals"]:
                for number in range(1, 20):
                    ingredient_key = f"strIngredient{number}"
                    measure_key = f"strMeasure{number}"
                    ingredient_value = meal.get(ingredient_key)
                    measure_value = meal.get(measure_key)
                    if ingredient_value:  # Check if the ingredient is not empty
                        # If measure is provided, include it along with the ingredient
                        if measure_value:
                            ingredients_text += f"{measure_value} {ingredient_value}, "
                        else:
                            ingredients_text += f"{ingredient_value}, "

            # Remove the trailing comma and space
            ingredients_text = ingredients_text.rstrip(", ")

            await message.reply(
                f"Good\n"
                f"<b>Name :</b> {name}\n\n"
                f"<b>🖼 Image :</b><a href='{thumbnail}'> Click here</a>\n\n"
                f"<b>Category :</b> {category}\n\n"
                f"<b>Area :</b> {area}\n\n"
                f"<b>Instruction :</b> {instruction}\n\n"
                f"<b>Ingredients :</b> {ingredients_text}\n\n"
                f"<b>Youtube :</b> {youtube}\n",
                parse_mode=types.ParseMode.HTML
            )
            await message.reply("If you want to cancel, type /cancel command.")
    else:
        await message.reply("No results found 😔.")
