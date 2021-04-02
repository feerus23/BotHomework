import sqlite3 as sql
import toml
import datetime as dt

cfg = toml.load('config.toml')

tvar = cfg['admins_id']; admin = []
for _, v in tvar.items(): admin.append(v)
del tvar

con = sql.connect('BotData\\data\\base\\base.sqlite')
curs = con.cursor()

def saveCFG(cfg):
    toml.dump(cfg, 'config.toml')

def checkDatabase():
    'Checking database function'
    try:
        curs.execute('SELECT * FROM users')
    except sql.OperationalError:
        query = [ 
            '''CREATE TABLE IF NOT EXISTS users (
                id INT(32) NOT NULL PRIMARY KEY,
                permission INT(2) NOT NULL,
                grade VARCHAR(3)
            );''', 
            '''CREATE TABLE IF NOT EXISTS schedule (
                day_of_week INT(1) NOT NULL PRIMARY KEY ON CONFLICT REPLACE,
                les_1st VARCHAR(128),
                les_2nd VARCHAR(128),
                les_3rd VARCHAR(128),
                les_4th VARCHAR(128),
                les_5th VARCHAR(128),
                les_6th VARCHAR(128)
            );''', 
            '''CREATE TABLE IF NOT EXISTS homework (
                day_of_week INT(1) REFERENCES schedule (day_of_week),
                date DATE(10) NOT NULL UNIQUE ON CONFLICT REPLACE,
                les_1st VARCHAR(128),
                les_2nd VARCHAR(128),
                les_3rd VARCHAR(128),
                les_4th VARCHAR(128),
                les_5th VARCHAR(128),
                les_6th VARCHAR(128)
            );''',
            '''CREATE TABLE IF NOT EXISTS titles (
                permission INT(2) NOT NULL PRIMARY KEY ON CONFLICT REPLACE,
                name CHAR(128) NOT NULL UNIQUE
            )'''
        ]

        for q in query: curs.execute(q); con.commit()

        return False
    else:
        return True

def isAdmin(perm):
    if perm >= cfg['admin']['min'] or perm == 0:
        return True
    else:
        return False

def ipairs(array):
    counter = 0
    while len(array) > counter:
        index, value = counter, array[counter]
        counter += 1
        yield index, value

def WeekdayToDate(from_date, search_day):
    from_date = from_date.replace(day=from_date.day - 1)
    from_day = from_date.isoweekday()

    different_days = search_day - from_day if from_day < search_day else 7 - from_day + search_day
    return from_date + dt.timedelta(days=different_days)

def eValue2int(array) -> list:
    second_array = list()

    for value in array:
        second_array.append(int(value))
    
    return second_array

def strToDate(array):
    # pylint: disable=unbalanced-tuple-unpacking
    a, b, c = eValue2int(array)
    return a, b, c

tfDict = {
    'Понедельник': 1,
    'Вторник': 2,
    'Среда': 3,
    'Четверг': 4,
    'Пятница': 5,
    'Суббота': 6
}

def tfDowSQL(string):
    return tfDict.get(string, False)

def tfDowStr(integer):
    return { v:k for k, v in tfDict.items() }.get(integer, False)