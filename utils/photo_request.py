from data.settings import headers
import aiohttp
from loader import logger


async def get_hotel_images(hotel_id: int, num_of_images: int = 5) -> list:
    """
    Корутина возвращающая фотографии отеля по его id

    :param hotel_id: id отеля
    :param num_of_images: количество фотографий
    :return: список с url фотографий отеля
    """

    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": hotel_id}
    images_list = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=headers, params=querystring) as resp:
                result = await resp.json()

        if num_of_images > len(result["hotelImages"]):
            num_of_images = len(result["hotelImages"])

        images_list = [image["baseUrl"].replace('{size}', 'b') for image in result["hotelImages"][0:num_of_images]]

    except Exception as e:
        logger.error(str(e.__class__) + ' ' + str(e))

    return images_list


async def add_hotel_images(hotels, num_of_images):
    """

    Корутина, добавляющая в список с отелями фотографии этих же отелей

    :param hotels: список словарей с информацией об отелях

    :param num_of_images: нужное количество фотографий

    :return: обновленный список отелей с фотографиями

    """
    if num_of_images != 0:
        for hotel in hotels:
            hotel["images"] = await get_hotel_images(hotel["hotel_id"], num_of_images)

    return hotels
