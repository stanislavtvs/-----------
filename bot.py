import asyncio
from asgiref.sync import async_to_sync

from aiogram import Bot, types, Dispatcher
from aiogram.filters import Command, CommandObject

from functions import DataBaseInterface


TOKEN = "7695738026:AAEN0h0QW4nhxQbPaHCjpGf7TxDukt9X_T8"

database = DataBaseInterface()
async_to_sync(database.connect)("data.db")

bot = Bot(token=TOKEN)
dispatcher = Dispatcher()


@dispatcher.message(Command("alabala"))
async def start(message: types.Message, command: CommandObject):
    print(command.args)
    await message.reply("Хай")
    await message.answer("OK")


@dispatcher.message(Command("контакт", prefix="+"))
async def add_contact(message: types.Message, command: CommandObject):
    user_id = message.from_user.id
    command_arguments = command.args.split(" ")
    contact_name = command_arguments[0]
    contact_number = command_arguments[1]

    await database.add_contact(user_id, contact_name, contact_number)
    await message.reply("Контакт успешно добавлен!")


async def main():
    await database.create_tables()
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
