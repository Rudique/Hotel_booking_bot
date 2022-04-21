from loader import logger
import aiohttp
from data.settings import headers, url


async def get_destination_id(city: str) -> int or None:
    """
    Корутина, возвращающая id города по его названию и
    проверяющая введенные данные на корректность

    :param city: название города

    :return: id города в hotelsAPI
    """
    querystring = {"query": city, "locale": "ru_RU"}

    try:

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=querystring) as resp:
                response = await resp.json()

        if len(response) == 0 or len(response["suggestions"][0]["entities"]) == 0:
            return None

        return response["suggestions"][0]["entities"][0]["destinationId"]

    except Exception as e:
        logger.error(str(e.__class__) + ' ' + str(e))
        return None




