async def check_dates(first_date: str, second_date: str):
    """
    Корутина, проверяющая две даты на очередность
    (вторая должна быть позже первой)

    :param first_date: первая дата

    :param second_date: вторая дата

    :return True или False
    """

    if int(first_date[0:4]) > int(second_date[0:4]):
        return False
    elif int(first_date[5:7]) > int(second_date[5:7]) and int(first_date[0:4]) == int(second_date[0:4]):
        return False
    elif int(first_date[5:7]) == int(second_date[5:7]) and int(first_date[0:4]) == int(second_date[0:4])\
            and int(first_date[8:10]) >= int(second_date[8:10]):
        return False
    else:
        return True
