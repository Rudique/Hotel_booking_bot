from loader import logger


async def price_check(prices: str) -> list or None:
    """
    Корутина, проверяющая корректность введенных
    цен или расстояний до центра

    :param prices: цены или расстояния до центра
    :return: список цен или дипазон расстояний до центра
    """

    try:
        res = [float(x) for x in prices.split('-')]
        return sorted(res)
    except Exception as e:
        logger.error(str(e.__class__) + ' ' + str(e))
        return None
