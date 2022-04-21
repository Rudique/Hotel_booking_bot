from loader import dp, logger
from aiogram.types import InputMediaPhoto
import types


async def message_sender(hotel_dict: dict, chat_id: int, days: int) -> str:
    """
    Корутина, формирующая информационное сообщение об отеле

    :param hotel_dict: словарь с данными об отеле
    :param chat_id: id чата переписки
    :param days: количество дней отпуска
    :return: возвращает текст информационного сообщения
    """

    result = ''

    distance = round(float(hotel_dict['distance']), 1)
    link = f'https://ru.hotels.com/ho{hotel_dict["hotel_id"]}'

    result += f"Название: {hotel_dict['name']}\n" \
              f"Адрес: {hotel_dict['address']}\n" \
              f"Расстояние до центра: {distance} км\n" \
              f"Цена за отпуск: ${int(hotel_dict['price'][1:].replace(',', '')) * days}\n" \
              f"Цена за ночь: {hotel_dict['price']}\n"\
              f"{link}\n"

    await dp.bot.send_message(chat_id=chat_id, text=result, disable_web_page_preview=True)

    if 'images' in hotel_dict.keys():

        media = [InputMediaPhoto(photo_url) for photo_url in hotel_dict['images']]

        try:
            await dp.bot.send_media_group(chat_id=chat_id, media=media)
        except Exception as e:
            logger.error(str(e.__class__) + ' ' + str(e))

    return result
