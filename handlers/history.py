from aiogram.dispatcher.filters import Command
from loader import dp, db, logger
from aiogram import types


@dp.message_handler(Command('history'))
async def help_command(message: types.Message):
    """
    Корутина, которая получает на вход команду /history
    и выводит историю запросов пользователя

    :param message: объект класса Message содержит
    в себе информацио о чате и пользователе
    """

    logger.info(f"User: {message.from_user.id} Command: {message.text}")

    history = await db.select_all_users()
    check = True
    if len(history) > 0:
        for elem in history:
            if elem[0] == int(message.from_user.id):
                await dp.bot.send_message(chat_id=message.from_user.id,
                                          text=elem[1],
                                          disable_web_page_preview=True)
                check = False

    if check:
        await dp.bot.send_message(chat_id=message.from_user.id,
                                  text='К сожалению не удалось ничего найти')
