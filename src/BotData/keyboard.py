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
        .add(Text('Расписание', {'cmd': 'sedit_menu'}))
        .add(Text('Домашнее задание', {'cmd': 'homework_menu'}))
        .row()
        .add(Callback('Администраторская панель', {'cmd': 'admin_menu'}), KeyboardButtonColor.NEGATIVE)
        .get_json()
    )

def schedule_menu():
    return (
        Keyboard(one_time = True)
        .add(Text('Изменить расписание', {'cmd': 'sedit_menu'}))
        .row()
        .add(Text('Назад', {'cmd': 'undo'}), KeyboardButtonColor.PRIMARY)
        .get_json()
    )

def sedit_menu():
    return (
        Keyboard(one_time = True)
        .add(Text('Понедельник', {'cmd': 'cws_menu'}))
        .add(Text('Вторник', {'cmd': 'cws_menu'}))
        .row()
        .add(Text('Среда', {'cmd': 'cws_menu'}))
        .add(Text('Четверг', {'cmd': 'cws_menu'}))
        .add(Text('Пятница', {'cmd': 'cws_menu'}))
        .row()
        .add(Text('Суббота', {'cmd': 'cws_menu'}))
        .row()
        .add(Text('Назад', {'cmd': 'undo'}), KeyboardButtonColor.PRIMARY)
        .get_json()
    )

def cls_menu():
    return (
        Keyboard(one_time = True)
        .add(Text('1 урок', {'cmd': 'cls_menu'}))
        .row()
        .add(Text('2 урок', {'cmd': 'cls_menu'}))
        .add(Text('3 урок', {'cmd': 'cls_menu'}))
        .row()
        .add(Text('4 урок', {'cmd': 'cls_menu'}))
        .add(Text('5 урок', {'cmd': 'cls_menu'}))
        .add(Text('6 урок', {'cmd': 'cls_menu'}))
        .row()
        .add(Text('Назад', {'cmd': 'undo'}), KeyboardButtonColor.PRIMARY)
        .get_json()
    )

def cls_menu_apply():
    return (
        Keyboard(one_time = True)
        .add(Text('1 урок', {'cmd': 'cls_menu'}))
        .row()
        .add(Text('2 урок', {'cmd': 'cls_menu'}))
        .add(Text('3 урок', {'cmd': 'cls_menu'}))
        .row()
        .add(Text('4 урок', {'cmd': 'cls_menu'}))
        .add(Text('5 урок', {'cmd': 'cls_menu'}))
        .add(Text('6 урок', {'cmd': 'cls_menu'}))
        .row()
        .add(Text('Применить', {'cmd': 'apply'}), KeyboardButtonColor.POSITIVE)
        .row()
        .add(Text('Назад', {'cmd': 'undo'}), KeyboardButtonColor.PRIMARY)
        .get_json()
    )

def undo_button():
    return (
        Keyboard(one_time = True)
        .add(Text('Назад', {'cmd': 'undo'}), KeyboardButtonColor.PRIMARY)
        .get_json()
    )