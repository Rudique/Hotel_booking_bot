from aiogram import executor, Dispatcher
from utils.set_bot_comands import set_default_commands
from loader import dp, db, logger
import handlers


async def on_startup(dp: Dispatcher):
    """
    Корутина создает бд Users и устанавливает
    меню команд бота при запуске модуля app.py

    :param dp: объект класса Dispatcher отлавливает все обновления от API телеграм
    """

    try:
        await db.create_table_users()

    except Exception as e:
        logger.error(str(e.__class__) + ' ' + str(e))

    await set_default_commands(dp)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
