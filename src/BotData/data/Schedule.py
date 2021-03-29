from .data import curs, con, tfDowSQL, tfDowStr

ORIGINAL = 0
MODIFIED = 1

class Schedule:
    'Класс для работы с расписанием'

    standart = [ i for i in range(1,7) ]
        
    def __init__(self, days_of_week):
        'Эээ... Метод инициализации-кун?'

        self.res = [ None ]
        self.aRes = [ None ]
        for i in range(1,7):
            self.res += [ [ i ] + [ None for i in range(0, 6) ] ]
            self.aRes += [ [ i ] + [ None for i in range(0, 6) ] ]
        
        
        self.dow = []
        
        if type(days_of_week) == str: days_of_week = [ tfDowSQL(days_of_week) ]
        elif type(days_of_week) == int: days_of_week = [ days_of_week ]

        for day in days_of_week:
            if not (day in self.standart):
                if not (day := tfDowSQL(day)):
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
            return tfDowStr(self.dow[0])
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