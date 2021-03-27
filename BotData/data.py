import sqlite3 as sql
import toml
import asyncio

tvar = toml.load('config.toml')['admins_id']; admin = []
for _, v in tvar.items(): admin.append(v)
del tvar

con = sql.connect('BotData\\base.sqlite')
curs = con.cursor()

ORIGINAL = 0
MODIFIED = 1

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
                day_of_week CHAR(3) NOT NULL PRIMARY KEY,
                date DATE(10) NOT NULL UNIQUE ON CONFLICT REPLACE,
                les_1st VARCHAR(128),
                les_2nd VARCHAR(128),
                les_3rd VARCHAR(128),
                les_4th VARCHAR(128),
                les_5th VARCHAR(128),
                les_6th VARCHAR(128)
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
    
    def vDel(self, *args):
        if len(args) == 1:
            del self.__Vars[args[0]]
        else:
            for v in args:
                del self.__Vars[v]

class Schedule:
    'Класс для работы с расписанием'

    standart = [ i for i in range(1,7) ]

    res = [ None ]
    aRes = [ None ]
    for i in range(1,7):
        res += [ [ i ] + [ None for i in range(0, 6) ] ]
        aRes += [ [ i ] + [ None for i in range(0, 6) ] ]
    
    
    dow = []

    __tfDict = {
        'Понедельник': 1,
        'Вторник': 2,
        'Среда': 3,
        'Четверг': 4,
        'Пятница': 5,
        'Суббота': 6
    }

    def __tfDowSQL(self, string):
        return self.__tfDict.get(string, False)

    def __tfDowStr(self, integer):
        return { v:k for k, v in self.__tfDict.items() }.get(integer, False)
        

    def __init__(self, days_of_week):
        def __tempFunc():
            curs.execute('SELECT * FROM schedule WHERE day_of_week = ?', (days_of_week,))
            if ftch := curs.fetchone():
                self.res[days_of_week] = list(ftch)
                #self.aRes = self.res.copy()
        
        if type(days_of_week) == str:
            self.dow = [ self.__tfDowSQL(days_of_week) ]
            __tempFunc()
        elif type(days_of_week) == int:
            self.dow = [ days_of_week ]
            __tempFunc()
        elif type(days_of_week) == list:
            for day in days_of_week:
                if not (day in self.standart):
                    if not (day := self.__tfDowSQL(day)):
                        break
                self.dow.append(day)

            if len(self.dow) != len(days_of_week): 
                #return 
                pass

            for day in self.dow:
                curs.execute('SELECT * FROM schedule WHERE day_of_week = ?', (day,))
                if ftch := curs.fetchone():
                    self.res[day] = list(ftch)
            
            #self.aRes = self.res.copy()

            #return
    
    def getRes(self, fl = ORIGINAL):
        if fl == ORIGINAL:
            res = self.res
        elif fl == MODIFIED:
            res = self.aRes
        return res
    

    def __getLesDict(self, days_of_week = None, lessons_numbers = None, from_list = ORIGINAL):
        if days_of_week is None: days_of_week = self.dow.copy()
        if lessons_numbers is None: lessons_numbers = self.standart.copy()

        if type(lessons_numbers) == int: lessons_numbers = [ lessons_numbers ]
        if type(days_of_week) == int: days_of_week = [ days_of_week ]

        if from_list == ORIGINAL:
            res = self.res.copy()
        elif from_list == MODIFIED:
            res = self.aRes.copy()

        lessons = {}
        for day in days_of_week:
            lessons.update([(day, {})])

            for les in lessons_numbers:
                if not (value := res[day][les]):
                    value = 'Нет данных'
                lessons[day].update([(les, value)])
                
        return lessons, days_of_week, lessons_numbers
    
    def getLesson(self, days_of_week = None, lessons_numbers = None, from_list = ORIGINAL) -> str:
        result, dow, _ = self.__getLesDict(days_of_week, lessons_numbers, from_list)

        string = str()

        for day in dow:
            tlen_1, tlen_2 = 0, 0
            for les, val in result[day].items():
                tlen_1 += 1
                if tlen_1 != len(result[day]):
                    string += str(les) + ') ' + val + '\n'
                else:
                    string += str(les) + ') ' + val
            
            if tlen_2:
                string += '\n'
            
            tlen_2 += 1
        
        return string
    
    def setLesson(self, days_of_week, lesson_number, value):
        self.aRes[days_of_week][lesson_number] = value
    
    def compare(self, days_of_week = None, lesson_numbers = None):
        #if len(self.res) != len(self.aRes): return False
        if days_of_week is None: days_of_week = self.dow
        if lesson_numbers is None: lesson_numbers = self.standart

        if type(lesson_numbers) == int: lesson_numbers = [ lesson_numbers ]

        for day in days_of_week:
            difference = False

            for les in lesson_numbers:
                if self.aRes[day][les] != self.res[day][les] and self.aRes[day][les] is not None:
                    difference = True
                    break
    
        return difference
    
    def isEmpty(self):
        tog = True

        for day in self.res:
            if not (day is None): 
                if not (day[0] is None):
                    for les in day:
                        if les != None and type(les) != int:
                            tog = False
        
        return tog
    
    def getDow(self, mode = 1):
        if mode == 1:
            return self.__tfDowStr(self.dow[0])
        elif mode == 2:
            return self.dow

    def merge(self):
        cRes, caRes = self.res.copy(), self.aRes.copy()
        result = cRes.copy()

        for day in self.dow:
            for i in range(1, len(caRes)):
                if caRes[day][i] != cRes[day][i] and caRes[day][i] != None:
                    result[day][i] = caRes[day][i]

        return result

    def save(self, days_of_week = None):
        if days_of_week is None: days_of_week = self.dow
        values = self.merge()

        for day in days_of_week:
            query = 'INSERT OR REPLACE INTO schedule VALUES (?, ?, ?, ?, ?, ?, ?)'
            curs.execute(query, tuple(values[day]))
        
        con.commit()

        #self.__init__(days_of_week)
    
    def update(self):
        pass