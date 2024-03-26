from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Restart the bot"),
            types.BotCommand("help", "Help"),
            types.BotCommand("random", "Random recipe"),
            types.BotCommand("search","Search meal")
        ]
    )
