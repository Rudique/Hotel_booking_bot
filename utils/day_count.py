from datetime import datetime


async def vacation_counter(date_one: str, date_two: str) -> int:
    """
    Корутина, которая подсчитывает количество дней между двумя датами

    :param date_one: первая дата
    :param date_two: вторая дата
    :return: разница м/у датами
    """

    date1 = datetime(day=int(date_one[8:10]), month=int(date_one[5:7]), year=int(date_one[0:4]))
    date2 = datetime(day=int(date_two[8:10]), month=int(date_two[5:7]), year=int(date_two[0:4]))

    return (date2 - date1).days
