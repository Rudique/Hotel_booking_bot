import aiosqlite


class Database:
    """
    Класс для работы с базой данных
    """

    def __init__(self, path_to_db='data/history.db'):
        self.path_to_db = path_to_db

    @property
    async def connection(self):
        """
        Метод класса который совершает подключение к бд

        :return: объект подключения к бд
        """

        return await aiosqlite.connect(self.path_to_db)

    async def execute(self, sql: str, params: tuple = None, fetchone=False,
                      fetchall=False, commit=False):
        """
        Метод класса выполняющий sql запросы

        :param sql: запрос на языке sql
        :param params: параметры, вставляемые в запрос
        :param fetchone: параметр, определяющий возвращать ли одну строку
        :param fetchall: параметр, определяющий возвращать все строки
        :param commit: параметр, определяющий делать ли запись в бд
        :return: данные бд
        """

        if not params:
            params = tuple()
        connection = await self.connection
        await connection.set_trace_callback(logger)
        cursor = await connection.cursor()
        await cursor.execute(sql, params)
        data = None

        if commit:
            await connection.commit()
        if fetchone:
            data = await cursor.fetchone()
        if fetchall:
            data = await cursor.fetchall()
        await cursor.close()
        await connection.close()
        return data

    async def create_table_users(self):
        """
        Метод, создающий таблицу Users
        """

        sql = """
        CREATE TABLE Users(
        id int NOT NULL,
        history varchar(1000)
        );

        """

        await self.execute(sql, commit=True)

    async def add_history(self, user_id, data):
        """
        Метод добавляющий результат запроса пользователя и его id

        :param user_id: id пользователя
        :param data: результат поиска
        :return:
        """

        sql = "INSERT INTO Users(id, history) VALUES(?, ?)"
        parameters = (user_id, data)
        await self.execute(sql, parameters, commit=True)

    async def select_all_users(self):
        """
        Метод возвращающий список с данными всей таблицы

        :return: данные таблицы Users
        """

        sql = "SELECT * FROM Users"
        result = await self.execute(sql, fetchall=True)
        return result


def logger(statement):
    """
    Функция для визуализации работы бд

    :param statement: текущая выполняемая задача бд
    """

    print(f"""
--------------------------------------------------------------------
Executing:
{statement}

____________________________________________________________________
""")
