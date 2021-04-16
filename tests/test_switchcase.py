import pytest
from src.body.features.switchcase import switch


def test_switch_list():
    var: list = [4, 9, 2, 7]

    for case in switch(var):
        if case(4):
            print('Wow, number is equal 4')


def test_switch_string():
    var: str = 'Okay'

    for case in switch(var):
        if case('String1'):
            print('Wow, this variable is string and equal String1')
        if case('Okay'):
            print('Wow this Okay')