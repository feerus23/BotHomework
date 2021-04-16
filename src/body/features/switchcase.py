def switch(cases, switch_type=None):
    def case(iter_value):
        def _case(_value):
            return _value == iter_value

        return _case

    if switch_type is None:
        print(type(cases))
        if (type(cases) == list) or (type(cases) == tuple):
            for value in cases:
                yield case(value)
        else:
            print('stop it')
            yield case(cases)
    else:
        yield case(cases)
