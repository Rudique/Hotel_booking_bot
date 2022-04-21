async def sort_by_destination_to_city_center(hotels: list, destination_to_city_center: list):
    """
    Корутина, которая возвращает из списка отелей
    подходящие по удалению от центра города

    :param hotels: список отелей

    :param destination_to_city_center: расстояния до центра города

    :return: сортированый список отелей
    """

    result = []
    for hotel in hotels:
        if destination_to_city_center[0] < hotel['distance'] < destination_to_city_center[1]:
            result.append(hotel)

    return result
