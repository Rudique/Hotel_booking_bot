from aiogram import types, Dispatcher


async def set_default_commands(dp: Dispatcher):
    """
    Корутина добавляющая меню с командами бота

    :param dp: объект класса Dispatcher отслеживающий обновления от API телеграма
    """

    await dp.bot.set_my_commands([types.BotCommand("lowprice", "поиск самых дешевых отелей"),
                                  types.BotCommand("highprice", "поиск самых дорогих отелей"),
                                  types.BotCommand("bestdeal", "поиск отелей по цене"),
                                  types.BotCommand("history", "история поиска"),
                                  types.BotCommand("help", "список команд бота")])
