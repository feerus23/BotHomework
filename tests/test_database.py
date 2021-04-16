import pytest

from src.body.data.classes.dynamic.database import DBConstruct


def test_dbconstruct_insert():
    var_dict = \
        {
            'table':
                {
                    'column_id': '44',
                    'column_name': 'Col_Name'
                }
        }

    insert_query = DBConstruct(var_dict).create()

    assert insert_query
    print(insert_query)
