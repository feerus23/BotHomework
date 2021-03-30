import datetime

def greeting():
    now = datetime.datetime.now()

    if now.hour in range(0, 6):
        return 'Доброй ночи'
    elif now.hour in range(6, 12):
        return 'Доброе утро'
    elif now.hour in range(12, 18):
        return 'Добрый день'
    elif now.hour in range(18, 24):
        return 'Добрый вечер'