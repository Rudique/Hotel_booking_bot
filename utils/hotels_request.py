from data.settings import headers
from data.settings import querystring_pattern
import aiohttp
from loader import logger


async def query_gen_func(sort_type: str,
                         destination_id: int,
                         arrive: str,
                         departure: str,
                         best_deal_price: tuple = (0, 0)
                         ):
    """
    Корутина формирующая словарь для запроса к hotelsApi

    :param sort_type: тип сортировки отелей по цене
    :param destination_id: id города, в котором производится поиск
    :param arrive: дата заезда
    :param departure: дата отъезда
    :param best_deal_price: ценовой диапозон
    :return: словарь для запроса к hotelsApi
    """

    query_pattern = dict(querystring_pattern)
    query_pattern["destinationId"] = destination_id
    query_pattern["checkIn"] = arrive
    query_pattern["checkOut"] = departure

    if sort_type == "lowprice":
        query_pattern["sortOrder"] = "PRICE"
        return query_pattern

    elif sort_type == "highprice":
        query_pattern["sortOrder"] = "PRICE_HIGHEST_FIRST"
        return query_pattern

    elif sort_type == "bestdeal":
        query_pattern["priceMin"] = str(int(best_deal_price[0]))
        query_pattern["priceMax"] = str(int(best_deal_price[1]))
        return query_pattern


async def get_json_function(sort_type: str,
                            destination_id: int,
                            arrive: str,
                            departure: str,
                            prices: tuple = (0, 0)
                            ):
    """
    Корутина отправляющая запрос к hotelsApi по параметрам

    :param sort_type: тип сортировки отелей по цене
    :param destination_id: id города, в котором производится поиск
    :param arrive: дата заезда
    :param departure: дата отъезда
    :param prices: ценовой диапозон
    :return: результат запроса к hotelsApi
    """

    querystring = await query_gen_func(sort_type, destination_id, arrive, departure, prices)
    url = "https://hotels4.p.rapidapi.com/properties/list"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=headers, params=querystring) as resp:
                response = await resp.json()

        return response["data"]["body"]["searchResults"]["results"]
    except Exception as e:
        logger.error(str(e.__class__) + ' ' + str(e))
