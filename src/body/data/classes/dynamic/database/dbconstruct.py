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
    def __init__(self, parse_dict=None):
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
                    length_2: int = 0
                    query[-1] += f'{k_1} '

                    for v_2 in v_1:
                        length_2 += 1

                        query[-1] += f'{v_2} ' if length_2 < len(v_1) else f'{v_2}'

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

    def select(self):
        """Метод для создания запроса SELECT FROM WHERE (WHERE необяз. параметр)
        example: { 'table': [ ('column_name', variable), 'VALUE_1', 'VALUE_2' ... 'VALUE_N' ] }
        0 индекс списка таблицы всегда соотвествует параметру WHERE. Если запрос не
        должен содержать WHERE, в качестве 0 индекса передавайте None"""
        query: list = []
        value: list = []

        for k, v in self.parse_dict.items():
            length: int = 0
            values = str()
            where = str()

            for v_1 in v:
                length += 1

                if v_1 is not None:
                    if v.index(v_1) == 0:
                        where = f' WHERE {v_1[0]} = ?'
                        value.append(v_1[1])
                    else:
                        values += f'{v_1}, ' if length < len(v) else f'{v_1}'

            query.append(f'SELECT {values} FROM {k}{where}')

        return query, value
