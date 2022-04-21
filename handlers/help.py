from aiogram.dispatcher.filters import Command
from loader import dp, logger
from aiogram import types


@dp.message_handler(Command('help'))
async def help_command(message: types.Message):
    """
    Корутина, которая получает на вход команду /help
    и выводит список команд бота пользователю

    :param message: объект класса Message содержит
    в себе информацио о чате и пользователе
    """

    logger.info(f"User: {message.from_user.id} Command: {message.text}")

    await dp.bot.send_message(chat_id=message.from_user.id,
                              text='Список команд бота:\n'
                                   '/lowprice - поиск самых дешевых отелей\n'
                                   '/highprice - поиск самых дорогих отелей\n'
                                   '/bestdeal - поиск отелей по цене и удалению от центра\n'
                                   '/history - история поиска\n'
                                   '/help - список команд бота'
                              )
