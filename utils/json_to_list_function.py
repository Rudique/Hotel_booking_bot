from loader import logger
import types


async def json_file_to_list_of_hotels(json_file: list) -> list:
    """
    Корутина обрабатывающая ответ от hotelsApi

    :param json_file: ответ от hotelsApi
    :return: Список словарей с информацией по отелям
    """

    hotels = []
    count_of_elem = 0
    for hotel in json_file:
        hotel_info = {}
        try:
            hotel_info["name"] = hotel["name"]
            hotel_info["hotel_id"] = hotel["id"]
            hotel_info["address"] = hotel["address"]["streetAddress"]
            hotel_info["distance"] = float(hotel["landmarks"][0]["distance"][:-6]) / 1.6
            hotel_info["price"] = hotel["ratePlan"]["price"]["current"]
            hotels.append(hotel_info)
            count_of_elem += 1
            if count_of_elem == 25:
                break
        except Exception as e:
            logger.error(str(e.__class__) + ' ' + str(e))

    return hotels
