from vkbottle import Keyboard, Text, Callback, KeyboardButtonColor

#main_tree
def begin_menu():
    return (
        Keyboard(one_time = True)
        .add(Text('Начать', {'cmd': 'main_menu'}))
        .get_json()
    )

def main_menu(mod='user'):
    if mod == 'user':
        return (
            Keyboard(one_time = True)
            .add(Text('Расписание', {'cmd': 'sedit_menu'}))
            .add(Text('Домашнее задание', {'cmd': 'homework_menu'}))
            .get_json()
        )
    elif mod == 'admin':
        return (
            Keyboard(one_time = True)
            .add(Text('Расписание', {'cmd': 'sedit_menu'}))
            .add(Text('Домашнее задание', {'cmd': 'homework_menu'}))
            .row()
            .add(Text('Администраторская панель', {'cmd': 'admin_menu'}), KeyboardButtonColor.POSITIVE)
            .get_json()
        )

#schedule_tree
def schedule_menu():
    return (
        Keyboard(one_time = True)
        .add(Text('Изменить расписание', {'cmd': 'sedit_menu'}))
        .row()
        .add(Text('Назад', {'cmd': 'undo_schedule'}), KeyboardButtonColor.PRIMARY)
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
        .add(Text('Назад', {'cmd': 'undo_schedule'}), KeyboardButtonColor.PRIMARY)
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
        .add(Text('Назад', {'cmd': 'undo_schedule'}), KeyboardButtonColor.PRIMARY)
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
        .add(Text('Назад', {'cmd': 'undo_schedule'}), KeyboardButtonColor.PRIMARY)
        .get_json()
    )

#admin_tree
def admin_menu():
    return (
        Keyboard(one_time = True)
        .add(Text('Посмотреть доступные уровни', {'cmd': 'al_shw_menu'}))
        .add(Text('Отредактировать уровень', {'cmd': 'al_upd_menu'}))
        .row()
        .add(Text('Выдать права доступа', {'cmd': 'adm_add_menu'}))
        .row()
        .add(Text('Назад', {'cmd': 'undo_admin'}), KeyboardButtonColor.PRIMARY)
        .get_json()
    )

#undo button
def undo_button(arg):
    return (
        Keyboard(one_time = True)
        .add(Text('Назад', {'cmd': 'undo_'+arg}), KeyboardButtonColor.PRIMARY)
        .get_json()
    )