from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from loader import dp, db, logger
from aiogram import types
from utils.destination_request import get_destination_id
from keyboards.hotels_keyboard import num_keyboard
from keyboards.photo_keyboards import photo_keyboard
import datetime
from utils.hotels_request import get_json_function
from utils.json_to_list_function import json_file_to_list_of_hotels
from utils.photo_request import add_hotel_images
from utils.answer_message_gen import message_sender
from utils.date_check import check_dates
from utils.day_count import vacation_counter
from utils.dialog_calendar import DialogCalendar, calendar_callback
from utils.prices_check import price_check
from utils.destination_sort_func import sort_by_destination_to_city_center


@dp.message_handler(Command(['lowprice', 'highprice', 'bestdeal']),  state=None)
async def any_price_command(message: types.Message, state: FSMContext):
    """
    Корутина с декоратором, который передает в нее все сообщения пользователей
    с командами /lowprice /highprice /bestdeal

    :param message: объект класса Message, содержащий в себе текст сообщения и
    информацию о чате и пользователе

    :param state: объект класса FSMContext содержит в себе состояние текущего
    пользователя и временно хранит в себе данные для отправки запроса в hotelsAPI
    и последующим добавлением в историю поиска
    """
    await dp.bot.send_message(chat_id=message.from_user.id,
                              text='Введите название интересующего вас города')

    await state.update_data(command=message.text[1:])

    logger.info(f"User: {message.from_user.id} Command: {message.text}")
    dt = str(datetime.datetime.now())[:-7]

    await state.update_data(datetime=dt)
    await state.set_state('set_city')


@dp.message_handler(state='set_city')
async def set_city(message: types.Message, state: FSMContext):
    """
    Корутина в которой выполняется проверка названия города на существование,
    также в зависимости от введенной ранее команды пользователя перенаправляет
    на выбор диапазона цен, либо дат отдыха. Декоратор передает в функцию
    текущее состояние пользователя

    :param message: объект класса Message, содержащий в себе текст сообщения и
    информацию о чате и пользователе

    :param state: объект класса FSMContext содержит в себе состояние текущего
    пользователя и временно хранит в себе данные для отправки запроса в hotelsAPI
    и последующим добавлением в историю поиска
    """
    city = message.text
    destination_id = await get_destination_id(city)
    data = await state.get_data()

    if destination_id is not None:

        await state.update_data(destination_id=destination_id)

        if data['command'] == 'bestdeal':
            await dp.bot.send_message(chat_id=message.from_user.id, text="Введите диапазон цен в USD,"
                                                                         " через дефис, например: 100-200")
            await state.set_state('set_price')
        else:
            await dp.bot.send_message(chat_id=message.from_user.id,
                                      text="Выберите дату прилета",
                                      reply_markup=await DialogCalendar().start_calendar())
            await state.update_data(prices=(0, 0))
            await state.set_state('arrive')

    else:
        await dp.bot.send_message(chat_id=message.from_user.id,
                                  text='Некорректное название, введите город,'
                                       ' в котором будет производиться поиск')


@dp.message_handler(state='set_price')
async def set_price(message: types.Message, state: FSMContext):
    """
    Корутина для ввода диапазона расстояний от отеля до центра города и
    проверки формата диапазона цен за ночь

    :param message: объект класса Message, содержащий в себе текст сообщения и
    информацию о чате и пользователе

    :param state: объект класса FSMContext содержит в себе состояние текущего
    пользователя и временно хранит в себе данные для отправки запроса в hotelsAPI
    и последующим добавлением в историю поиска
    """
    res = await price_check(message.text)
    if res is not None:
        await state.update_data(prices=res)
        await dp.bot.send_message(chat_id=message.from_user.id,
                                  text='Введите диапазон удаления от центра города через дефис'
                                       ' в км, например: 1.5-2')
        await state.set_state('set_distance')

    else:
        await dp.bot.send_message(chat_id=message.from_user.id,
                                  text='Некорректный формат. Введите диапазон '
                                       'цен в USD, через дефис, например: 100-200')


@dp.message_handler(state='set_distance')
async def set_distance(message: types.Message, state: FSMContext):
    """
    Корутина для ввода даты прилета и проверки диапазона расстояний до центра города

    :param message: объект класса Message, содержащий в себе текст сообщения и
    информацию о чате и пользователе

    :param state: объект класса FSMContext содержит в себе состояние текущего
    пользователя и временно хранит в себе данные для отправки запроса в hotelsAPI
    и последующим добавлением в историю поиска
    """
    res = await price_check(message.text)
    if res is not None:
        await state.update_data(distance=res)
        await dp.bot.send_message(chat_id=message.from_user.id,
                                  text="Выберите дату прилета",
                                  reply_markup=await DialogCalendar().start_calendar())

        await state.set_state('arrive')
    else:
        await dp.bot.send_message(chat_id=message.from_user.id,
                                  text='Некорректный формат. Введите диапазон удаления от центра города через дефис'
                                       ' в км, например: 1.5-2')


@dp.callback_query_handler(calendar_callback.filter(), state="arrive")
async def set_arrive_date(callback_query: types.CallbackQuery, callback_data, state: FSMContext):
    """
    Корутина для ввода даты отъезда и проверки дат на корректность

    :param callback_query: объект класса CallbackQuery с информацией
    о нажатой кнопке на инлайн клавиатуре

    :param callback_data: данные о дате прилета

    :param state: объект класса FSMContext содержит в себе состояние текущего
    пользователя и временно хранит в себе данные для отправки запроса в hotelsAPI
    и последующим добавлением в историю поиска
    """
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)

    if selected:
        test = await check_dates(str(datetime.date.today() - datetime.timedelta(days=1)), date.strftime("%Y-%m-%d"))
        if test:

            await state.update_data(arrive=date.strftime("%Y-%m-%d"))
            await dp.bot.send_message(chat_id=callback_query.from_user.id,
                                      text="Выберите дату отъезда домой",
                                      reply_markup=await DialogCalendar().start_calendar())
            await state.set_state('departure')
        else:
            await dp.bot.send_message(chat_id=callback_query.from_user.id,
                                      text="Дата заселения не может раньше, чем сегодня\n"
                                           "Выберите дату заселения",
                                      reply_markup=await DialogCalendar().start_calendar())


@dp.callback_query_handler(calendar_callback.filter(), state="departure")
async def set_departure_date(callback_query: types.CallbackQuery, callback_data, state: FSMContext):
    """
    Корутина для выбора количества отелей на вывод

    :param callback_query: объект класса CallbackQuery с информацией
    о нажатой кнопке на инлайн клавиатуре

    :param callback_data: данные о дате прилета

    :param state: объект класса FSMContext содержит в себе состояние текущего
    пользователя и временно хранит в себе данные для отправки запроса в hotelsAPI
    и последующим добавлением в историю поиска
    """
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        data = await state.get_data()

        test = await check_dates(data["arrive"], date.strftime("%Y-%m-%d"))
        if not test:
            await dp.bot.send_message(chat_id=callback_query.from_user.id,
                                      text="Дата отъезда не должна быть раньше прилета\n"
                                           "Выберите дату отъезда домой",
                                      reply_markup=await DialogCalendar().start_calendar())
        else:
            await state.update_data(departure=date.strftime("%Y-%m-%d"))

            await dp.bot.send_message(chat_id=callback_query.from_user.id,
                                      text='Выберите нужное количество отелей',
                                      reply_markup=num_keyboard)
            await state.set_state('set_num_of_hotels')


@dp.callback_query_handler(state='set_num_of_hotels')
async def set_num_of_hotels(callback: types.CallbackQuery, state: FSMContext):
    """
    Корутина для записи количества отелей на вывод и переводящая пользователя
    к определению нужны ли ему фотографии отелей

    :param callback: объект класса CallbackQuery с информацией
    о нажатой кнопке на инлайн клавиатуре

    :param state: объект класса FSMContext содержит в себе состояние текущего
    пользователя и временно хранит в себе данные для отправки запроса в hotelsAPI
    и последующим добавлением в историю поиска
    """
    await dp.bot.delete_message(chat_id=callback.from_user.id,
                                message_id=callback.message.message_id)
    await dp.bot.send_message(chat_id=callback.from_user.id,
                              text='Нужны ли Вам фотографии отелей?',
                              reply_markup=photo_keyboard)
    await state.update_data(hotels_num=callback.data)

    await state.set_state('photo')


@dp.callback_query_handler(state='photo')
async def set_photo(callback: types.CallbackQuery, state: FSMContext):
    """
    Корутина в которой определяется нужны ли фотографии отелей пользователю
    в противном случае выводит информацию о найденных отелях

    :param callback: объект класса CallbackQuery с информацией
    о нажатой кнопке на инлайн клавиатуре

    :param state: объект класса FSMContext содержит в себе состояние текущего
    пользователя и временно хранит в себе данные для отправки запроса в hotelsAPI
    и последующим добавлением в историю поиска
    """
    await dp.bot.delete_message(chat_id=callback.from_user.id,
                                message_id=callback.message.message_id)

    if callback.data == 'Yes':

        await dp.bot.send_message(chat_id=callback.from_user.id,
                                  text='Выберите нужное кол-во фотографий каждого отеля',
                                  reply_markup=num_keyboard)
        await state.update_data(photo=callback.data)
        await state.set_state('set_num_of_photo')

    elif callback.data == 'No':

        data = await state.get_data()

        json_file = await get_json_function(data['command'], data['destination_id'],
                                            data['arrive'], data['departure'], data['prices'])
        hotels = await json_file_to_list_of_hotels(json_file=json_file)

        days = await vacation_counter(data['arrive'], data['departure'])

        if data["command"] == 'bestdeal':
            hotels = await sort_by_destination_to_city_center(hotels, data['distance'])

        num = len(hotels) if len(hotels) < int(data['hotels_num']) else int(data['hotels_num'])

        if num == 0:
            await dp.bot.send_message(chat_id=callback.from_user.id,
                                      text='К сожалению по вашему запросу не удалось ничего найти')
            await state.reset_state(with_data=True)

        history = f"Команда: {data['command']}\n" \
                  f"Дата и время ввода: {data['datetime']}\n"

        for i in range(num):
            history += await message_sender(hotel_dict=hotels[i], chat_id=callback.from_user.id,
                                            days=days)

        await db.add_history(callback.from_user.id, history)

        await state.reset_state(with_data=True)


@dp.callback_query_handler(state='set_num_of_photo')
async def set_num_of_photo(callback: types.CallbackQuery, state: FSMContext):
    """
    Корутина получает количество нужных фотографий и отправляет ответ пользователю

    :param callback: объект класса CallbackQuery с информацией
    о нажатой кнопке на инлайн клавиатуре

    :param state: объект класса FSMContext содержит в себе состояние текущего
    пользователя и временно хранит в себе данные для отправки запроса в hotelsAPI
    и последующим добавлением в историю поиска
    """

    await dp.bot.delete_message(chat_id=callback.from_user.id,
                                message_id=callback.message.message_id)

    await dp.bot.send_message(chat_id=callback.from_user.id,
                              text='Происходит загрузка фотографий и информации об отелях,'
                                   ' это может занять некоторое время')

    await state.update_data(photo_num=callback.data)

    data = await state.get_data()

    json_file = await get_json_function(data['command'], data['destination_id'],
                                        data['arrive'], data['departure'], data['prices'])

    hotels = await json_file_to_list_of_hotels(json_file=json_file)

    hotels = await add_hotel_images(hotels, num_of_images=int(data['photo_num']))

    days = await vacation_counter(data['arrive'], data['departure'])

    if data["command"] == 'bestdeal':
        hotels = await sort_by_destination_to_city_center(hotels, data['distance'])

    num = len(hotels) if len(hotels) < int(data['hotels_num']) else int(data['hotels_num'])

    if num == 0:
        await dp.bot.send_message(chat_id=callback.from_user.id,
                                  text='К сожалению по вашему запросу не удалось ничего найти')
        await state.reset_state(with_data=True)

    history = f"Команда: {data['command']}\n" \
              f"Дата и время ввода: {data['datetime']}\n"
    for i in range(num):
        history += await message_sender(hotel_dict=hotels[i], chat_id=callback.from_user.id,
                                        days=days)

    await db.add_history(callback.from_user.id, history)

    await state.reset_state(with_data=True)
