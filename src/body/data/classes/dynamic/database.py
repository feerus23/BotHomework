import sqlite3 as sql
from src.body.data.storages.constants import DATABASE_PATH
from src.body.features.switchcase import switch

# QUERY TYPES
CREATE = 0
INSERT = 1
DROP = 2


class DBConstruct:
    """Парсер для преобразования словарей в SQL запросы. Спрашивается зачем? По приколу."""
    # Properties of class
    _parse_dict: dict = {}

    @property
    def parse_dict(self):
        return self._parse_dict

    @parse_dict.setter
    def parse_dict(self, value):
        self._parse_dict = value

    # Constructors of class
    def __init__(self, parse_dict=None) -> object:
        """В качестве parse_dict указывать словарь, в документации
        каждого метода указан пример словаря"""

        self.parse_dict = parse_dict

    # Methods of class
    def create(self):
        """Метод для запроса CREATE IF NOT EXISTS. Я кста быдло.
        example: { 'table': { 'col_id': ('INT(3)', 'NOT NULL', 'PRIMARY KEY'), 'col_name': 'value' }"""
        query = []

        for k, v in self.parse_dict.items():
            length: int = 0

            query.append(f'CREATE TABLE IF NOT EXISTS {k} (')

            for k_1, v_1 in v.items():
                length += 1

                if type(v_1) is str:
                    query[-1] += f'{k_1} {v_1}, ' if length < len(v) else f'{k_1} {v_1})'
                elif type(v_1) is tuple:
                    for v_2 in v_1:
                        query[-1] += f'{v_2} '

                    query[-1] += ', ' if length < len(v) else ')'

            return query

    def insert(self):
        """Метод для создания запроса INSERT OR REPLACE
        example: { 'table': { 'col_id': '5', 'col_name': 'some_another_value' }"""
        query: list = []
        values: tuple = ()

        for k, v in self.parse_dict.items():
            str_values: str = 'VALUES ('
            length: int = 0

            query.append(f'INSERT OR REPLACE INTO {k} (')

            for k_1, v_1 in v.items():
                length += 1

                if type(v_1) is str:
                    query[-1] += f'{k_1}, ' if length < len(v) else f'{k_1}) '

                values += (v_1,)
                str_values += '?, ' if length < len(v) else '?)'

            query[-1] += str_values

        return query, values


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

        for q in query:
            self._cursor.execute(q)

        if commit:
            self._connection.commit()

    def commit(self):
        self._connection.commit()
