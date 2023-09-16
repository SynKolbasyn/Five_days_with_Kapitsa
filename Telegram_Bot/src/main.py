import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, BotCommand

from functions import message_processing


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    handlers=[
        logging.FileHandler(filename="../game_data/logs/telegram_logs.log", mode="a"),
        logging.StreamHandler()
    ]
)


TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(TOKEN)

dp = Dispatcher()


async def setup_bot_commands(dispatcher):
    bot_commands = [
        BotCommand(command="/start", description="Show start menu"),
        BotCommand(command="/help", description="Show help menu")
    ]
    await bot.set_my_commands(bot_commands)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Tells the player about this bot: what it can do and what it is needed for

    :param message: message from player
    :return: None
    """

    await message.reply_photo(
        FSInputFile("../resources/images/start.png"),
        "A message that tells the player about this bot: what it can do and what it is needed for"
    )


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    """
    Tells the player how to use the bot

    :param message: message from player
    :return: None
    """

    await message.reply_photo(
        FSInputFile("../resources/images/help.png"),
        "A message that tells the player how to use the bot"
    )


@dp.message()
async def main_handler(message: Message) -> None:
    answer, image = await message_processing(message, bot)
    await message.reply_photo(image, answer)


async def main() -> None:
    await dp.startup.register(setup_bot_commands)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
