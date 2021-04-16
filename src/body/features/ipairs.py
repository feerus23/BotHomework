def ipairs(list_variable: list) -> tuple:
    index: int = 0

    while index < len(list_variable):
        yield index, list_variable[index]
        index += 1