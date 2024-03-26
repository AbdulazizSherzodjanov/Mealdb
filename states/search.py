from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import BoundFilter
class RecipeSearch(StatesGroup):
    search = State()