from vkbottle import Keyboard, Text, Callback, KeyboardButtonColor

__trees = {
    'schedule': ('cws_menu', 'cls_menu')
}

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

#admin_tree
def admin_menu():
    return (
        Keyboard(one_time = True)
        .add(Text('Посмотреть доступные уровни', {'cmd': 'al_shw_menu'}))
        .add(Text('Отредактировать уровень', {'cmd': 'al_upd_menu'}))
        .row()
        .add(Text('Выдать права доступа', {'cmd': 'adm_add_menu'}))
        .add(Text('Список пользователей', {'cmd': 'adm_list_menu'}))
        .row()
        .add(Text('Назад', {'cmd': 'undo_admin'}), KeyboardButtonColor.PRIMARY)
        .get_json()
    )

#homework_tree

#both schedule-homework
def sedit_menu(tree = 'schedule'):
    
    if payload := __trees.get(tree)[0]:
        return (
            Keyboard(one_time = True)
            .add(Text('Понедельник', {'cmd': payload}))
            .add(Text('Вторник', {'cmd': payload}))
            .row()
            .add(Text('Среда', {'cmd': payload}))
            .add(Text('Четверг', {'cmd': payload}))
            .add(Text('Пятница', {'cmd': payload}))
            .row()
            .add(Text('Суббота', {'cmd': payload}))
            .row()
            .add(Text('Назад', {'cmd': 'undo_' + tree}), KeyboardButtonColor.PRIMARY)
            .get_json()
        )
    else:
        raise ValueError('Input correct tree!')
    
def cls_menu(tree = 'schedule', mode = 'standart'):
    
    if payload := __trees.get(tree)[1]:
        temp = (
            Keyboard(one_time = True)
            .add(Text('1 урок', {'cmd': payload}))
            .row()
            .add(Text('2 урок', {'cmd': payload}))
            .add(Text('3 урок', {'cmd': payload}))
            .row()
            .add(Text('4 урок', {'cmd': payload}))
            .add(Text('5 урок', {'cmd': payload}))
            .add(Text('6 урок', {'cmd': payload}))
            .row() 
        )
    else:
        raise ValueError('Input correct tree!')

    if mode == 'standart':
        temp = (
            temp
            .add(Text('Назад', {'cmd': 'undo_'+tree}), KeyboardButtonColor.PRIMARY)
            .get_json()
        )
    elif mode == 'apply':
        temp = (
            temp
            .add(Text('Применить', {'cmd': 'apply_'+tree}), KeyboardButtonColor.POSITIVE)
            .row()
            .add(Text('Назад', {'cmd': 'undo_'+tree}), KeyboardButtonColor.PRIMARY)
            .get_json()
        )
    
    return temp

#undo button
def undo_button(arg):
    return (
        Keyboard(one_time = True)
        .add(Text('Назад', {'cmd': 'undo_'+arg}), KeyboardButtonColor.PRIMARY)
        .get_json()
    )