import pytest

from src.body.data.classes.dynamic.database import DBConstruct


def test_dbconstruct_create():
    var_dict = \
        {
            'table':
                {
                    'column_id': ('INT(8)', 'NOT NULL', 'PRIMARY KEY'),
                    'column_name': 'CHAR(32)'
                }
        }

    create_query = DBConstruct(var_dict).create()
    print(create_query)


def test_dbconstruct_insert():
    var_dict = \
        {
            'table':
                {
                    'column_id': '44',
                    'column_name': 'Col_Name'
                }
        }

    insert_query = DBConstruct(var_dict).insert()

    assert insert_query
    print(insert_query)


def test_dbconstruct_select():
    var_dict = \
        {
            'table':
                [
                    ('column_4', 12),
                    'column_1',
                    'column_2'
                ]
        }

    select_query = DBConstruct(var_dict).select()

    print(select_query)


def test_dbconstruct_select_with_none_zero_index():
    var_dict = \
        {
            'table':
                [
                    None,
                    'column_1',
                    'column_2'
                ]
        }

    select_query = DBConstruct(var_dict).select()

    print(select_query)
