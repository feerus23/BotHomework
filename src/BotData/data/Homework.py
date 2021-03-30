from .data import curs, con, tfDowSQL, tfDowStr, ipairs, WeekdayToDate, strToDate
from .Schedule import Schedule

import datetime as dt
import re

class Homework:

    def __init__(self, date):
        self.homework = dict()
        redate = re.findall(r'\d+', date)
        
        if len(redate) > 0:
            y, m, d = strToDate(redate)
        else:
            if week := tfDowSQL(date):
                date = str(WeekdayToDate(dt.date.today(), week))
                y, m, d = strToDate(re.findall(r'\d+', date))
            else:
                raise ValueError("Input correct date or weekday!")

        self.this = dt.date(y, m, d)
        self.weekday = self.this.isoweekday()

        curs.execute('SELECT * FROM homework WHERE date = ?', (self.this,))

        if res := curs.fetchone():
            for i, v in ipairs(res):
                if i > 1:
                    self.homework.update([(i-1, v)])
        else:
            for i in Schedule.standart:
                self.homework.update([(i, None)])
    
    def getHomework(self, lessons = None, mode = 0):
        if lessons is None:
            lessons = Schedule.standart
        elif isinstance(lessons, int):
            lessons = [ lessons ]
        
        string = str()
        array = list()

        counter = 0
        for les in lessons:
            counter += 1
            if lesson := (self.homework).get(les, 'Нет данных'):
                string += lesson
                array.append(lesson)
            else:
                string += 'Нет данных'
                array.append('Нет данных')

            if counter < len(lessons):
                string += '\n'

        return string if mode == 0 else array

    def getWeekday(self):
        return self.this.isoweekday()
    
    def getScheduleHomework(self, mode = 0):
        schedule, _, _ = Schedule(self.this.isoweekday())._getLesDict()
        homework = self.getHomework(mode = 1)

        result_list = list()
        result_string = str()

        cntr = 0
        for i in range(0, len(homework)):
            row = homework[i]
            cntr += 1

            if mode == 0:
                result_string += schedule[self.getWeekday()][i+1] + ': ' + row

                if cntr < len(homework):
                    result_string += '\n'
            else:
                result_list.append((schedule[homework.index(row)+1], row))
        
        return result_string 
    
    