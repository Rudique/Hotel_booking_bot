from aiogram.dispatcher.filters import Command
from loader import dp, logger
from aiogram import types


@dp.message_handler(Command('start'))
async def start_command(message: types.Message):
    """
    Корутина, в которую поступает команда /start, в ответ
    отправляет сообщение с командами бота

    :param message: объект класса Message содержит
    в себе информацио о чате и пользователе
    """

    logger.info(f"User: {message.from_user.id} Command: {message.text}")

    await dp.bot.delete_message(chat_id=message.from_user.id,
                                message_id=message.message_id)
    await dp.bot.send_message(chat_id=message.from_user.id,
                              text='Здравствуйте, я бот для поиска отелей в любом городе мира \n'
                                   '\n'
                                   'Список команд бота:\n'
                                   '/lowprice - поиск самых дешевых отелей\n'
                                   '/highprice - поиск самых дорогих отелей\n'
                                   '/bestdeal - поиск отелей по цене и удалению от центра\n'
                                   '/history - история поиска\n'
                                   '/help - список команд бота'
                              )
