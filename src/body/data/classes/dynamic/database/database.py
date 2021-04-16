import sqlite3 as sql
from src.body.data.storages.constants import DATABASE_PATH
from src.body.features.switchcase import switch
from .dbconstruct import DBConstruct

# QUERY TYPES
CREATE = 0
INSERT = 1
SELECT = 2
DROP = 3


class Database:
    """Database class"""
    # Class properties
    if True:
        _connection: sql.Connection
        _cursor: sql.Cursor
        _data: list

        @property
        def con(self):
            return self._connection

        @property
        def cur(self):
            return self._cursor

        @property
        def data(self):
            return self._data

    # Class constructors
    def __init__(self, path: str):
        """В качестве параметра принимает путь до БД"""
        self._connection = sql.connect(path)
        self._cursor = self.con.cursor()

    def exe_query(self, query_type, query_dict: dict, commit=False) -> None:
        """Метод выполнения запроса с использованием класса парсера DBConstruct.
        В качестве аргументов принимает
        query_type: CREATE, INSERT, DROP (DROP не реализован)
        query_dict - словарь с данными для парсинга
        commit - применить изменения сразу иль нет"""

        dbcobj = DBConstruct(query_dict)
        query = list()

        for case in switch(query_type):
            if case(CREATE):
                query = dbcobj.create()
            elif case(INSERT):
                query, values = dbcobj.insert()
            elif case(SELECT):
                query, value = dbcobj.select()

        for q in query:
            if type(q) != str:
                self._cursor.execute(q[0], q[1])
            else:
                self._cursor.execute(q)

        if commit:
            self._connection.commit()

    def commit(self):
        self._connection.commit()
