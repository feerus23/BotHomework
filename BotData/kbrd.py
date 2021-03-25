from vkbottle import Keyboard, Text, Callback, KeyboardButtonColor

def begin_menu():
    return (
        Keyboard(one_time = True)
        .add(Text('Начать', {'cmd': 'main_menu'}))
        .get_json()
    )

def main_menu():
    return (
        Keyboard(one_time = True)
        .add(Text('Расписание', {'cmd': 'schedule_menu'}))
        .add(Text('Домашнее задание', {'cmd': 'homework_menu'}))
        .row()
        .add(Callback('Администраторская панель', {'cmd': 'admin_menu'}), KeyboardButtonColor.PRIMARY)
        .get_json()
    )