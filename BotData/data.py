import sqlite3 as sql
import toml
import asyncio

tvar = toml.load('config.toml')['admins_id']; admin = []
for _, v in tvar.items(): admin.append(v)
del tvar

con = sql.connect('BotData\\base.sqlite')
curs = con.cursor()

def checkDatabase():
    'Checking database function'
    try:
        curs.execute('SELECT * FROM users')
    except sql.OperationalError:
        query = [ 
            '''CREATE TABLE IF NOT EXISTS users (
                id INT(32) NOT NULL PRIMARY KEY,
                permission INT(2) NOT NULL,
                grade VARCHAR(3) NOT NULL
            );''', 
            '''CREATE TABLE IF NOT EXISTS schedule (
                day_of_week INT(1) NOT NULL PRIMARY KEY,
                les_1st VARCHAR(127) NOT NULL,
                les_2nd VARCHAR(127) NOT NULL,
                les_3rd VARCHAR(127) NOT NULL,
                les_4th VARCHAR(127) NOT NULL,
                les_5th VARCHAR(127) NOT NULL,
                les_6th VARCHAR(127) NOT NULL
            );''', 
            '''CREATE TABLE IF NOT EXISTS homework (
                day_of_week CHAR(3) NOT NULL PRIMARY KEY,
                date DATE(10) NOT NULL UNIQUE,
                les_1st VARCHAR(127) NOT NULL,
                les_2nd VARCHAR(127) NOT NULL,
                les_3rd VARCHAR(127) NOT NULL,
                les_4th VARCHAR(127) NOT NULL,
                les_5th VARCHAR(127) NOT NULL,
                les_6th VARCHAR(127) NOT NULL
            );''',
            '''CREATE TABLE IF NOT EXISTS titles (
                permission INT(2) NOT NULL PRIMARY KEY,
                name CHAR(127) NOT NULL UNIQUE
            )'''
        ]

        for q in query: curs.execute(q)

        con.commit()

        return False
    else:
        return True

class Title:
    'Класс для получения или изменения данных о званиях (приурочены к уровням доступа)'

    def Set(self, **kwargs):
        curs.execute('SELECT * FROM titles'); titles = curs.fetchall()
        query = { 'insert': 'INSERT INTO titles (permission, name) VALUES (?, ?)', 'update': 'UPDATE titles SET name = ? WHERE permission = ?' }

        for k, v in kwargs:
            tumbler = False
            for t in titles:
                if k in t:
                    curs.execute(query['update'], str(v), k)
                    tumbler = True
            
            if tumbler: continue

            curs.execute(query['insert'], k, str(v))
        
        con.commit()

    def Get(self, permission):
        curs.execute('SELECT name FROM titles WHERE permission = ?', (permission,))

        if res := curs.fetchone():
            return res[0]
        else:
            return False, 'Нет звания к такому уровню доступа.'

class Users:
    'Класс для обработки пользовательских данных'

    Prm = {}
    tparams = { 'user_id': 0, 'permission': 1, 'grade': 2 }

    __Vars = {}

    __empty_list = [(1, None), (2, None)]

    def __init__(self, user_id):
        self.Prm[0] = user_id

        if checkDatabase():
            curs.execute('SELECT permission, grade FROM users WHERE id = ?', (user_id,))
            if res := curs.fetchone():
                self.Prm.update([(1, res[0]), (2, res[1])])
            else:
                if user_id in admin:
                    self.Prm.update([(1, 0), (2, '10b')])
                else:
                    self.Prm.update(self.__empty_list)
        else:
            if user_id in admin:
                self.Prm.update([(1, 0), (2, '10b')])
            else:
                self.Prm.update(self.__empty_list)

    def setParam(self, param, value):
        if type(param) == str:
            param = self.tparams[param]
        self.Prm[param] = value
    
    def getParam(self, param):
        if type(param) == str:
            param = self.tparams[param]
        try:
            return self.Prm[param]
        except KeyError:
            return None
    
    def updateData(self):
        curs.execute('SELECT permission, grade FROM users WHERE id = ?', (self.Prm[0],))
        if res := curs.fetchone():
            self.Prm[1] = res[0]; self.Prm[2] = res[1]
        else:
            return
    
    def saveData(self):
        'Сохраняет все значения пользователя. Понадобится при изменении уровня'
        curs.execute('UPDATE users SET permission = ?, grade = ? WHERE id = ?', (self.Prm[1], self.Prm[2], self.Prm[0]))
        curs.commit()
    
    def createUser(self, **kwargs):
        'Создаёт новую строку в таблице. Имена столбцов и их значения указываются в **kwargs'
        query = 'INSERT INTO users '
        columns = '(user_id, '; values = (); values_str = ' (?, '; cunt = 0

        for k, v in kwargs.items():
            cunt +=1

            if len(kwargs) > cunt:
                columns += str(k) + ', '
                values_str += '?, '
            else:
                columns += str(k) + ') '
                values_str += '?)'

            values += (v,)
        
        query += columns + 'VALUES' + values_str
        values = (self.Prm[0],) + values

        curs.execute(query, values)
        con.commit()

    def vSet(self, **kwargs):
        updates = ()

        if len(kwargs) == 1:
            k, v = list(kwargs.items())[0]
            self.__Vars.update([(k, v)])
            return v
            
        for k, v in kwargs.items():
            self.__Vars.update([(k, v)])
            updates += (v, )
        
        return updates
    
    def vGet(self, *args):
        retvals = ()

        if len(args) == 1:
            return self.__Vars.get(args[0], None)

        for v in args:
            retvals += (self.__Vars.get(v, None),)

        return retvals

class Schedule:
    'Класс для работы с расписанием'

    standart = [ i for i in range(1,7) ]
    aRes = [ None for i in range(1,8) ]
    res = []
    dow = []

    difference = False

    def __tfDowSQL(self, string):
        return {
            'понедельник': 1,
            'вторник': 2,
            'среда': 3,
            'четверг': 4,
            'пятница': 5,
            'суббота': 6
        }.get(string, False)

    def __init__(self, day_of_week):
        if type(day_of_week) == str:
            self.dow = [ self.__tfDowSQL(day_of_week) ]
        elif type(day_of_week) == int:
            self.dow = [ day_of_week ]
        elif type(day_of_week) == list:
            for day in day_of_week:
                if not (day in self.standart):
                    if not (day := self.__tfDowSQL(day)):
                        break
                self.dow.append(day)

            if len(self.dow) != len(day_of_week): 
                return 

            for day in self.dow:
                curs.execute('SELECT * FROM schedule WHERE day_of_week = ?', (day,))
                if ftch := curs.fetchone():
                    self.res.append(ftch)

            return

        curs.execute('SELECT * FROM schedule WHERE day_of_week = ?', (day_of_week,))
        if ftch := curs.fetchone():
            self.res.append(ftch)
    
    def getRes(self):
        return self.res

    def getLesson(self, lessons = standart, day_of_week = dow):
        'Функция возвращающая названия уроков списком.'
        if type(lessons) == int: lessons = [ lessons ]

        les_names = []

        for i in range(0, len(lessons)):
            try:
                tvar = self.res[lessons[i]]
            except IndexError:
                les_names.append(str(i+1) + ') Нет данных')
            else:
                if not tvar:
                    les_names.append(str(i+1) + ') Нет данных')
                else:
                    les_names.append(str(i+1) + ') ' + tvar)
        
        return les_names
    
    def getELesson(self, lessons = standart):
        pass
    
    def setLesson(self, lesson_number, name):
        self.aRes[lesson_number] = name
    
    def compare(self):
        if len(self.res) != len(self.aRes): return False

        for i in range(1, len(self.res)+1):
            if self.aRes[i] != self.res[i] and self.aRes[i] != None:
                self.difference = True
                break
    
        return self.difference
    
    def getDow(self):
        return self.dow