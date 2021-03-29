from .data import curs, con, tfDowSQL, tfDowStr, ipairs, WeekdayToDate, eValue2int
from .Schedule import Schedule

import datetime as dt
import re

class Homework:

    def __init__(self, date):
        self.homework = dict()
        redate = re.findall(r'\d+', date)
        
        if len(redate) > 0: 
            y, m, d = eValue2int(redate)
        else:
            if week := tfDowSQL(date):
                date = str(WeekdayToDate(dt.date.today(), week))
                y, m, d = eValue2int(re.findall(r'\d+', date))
            else:
                raise ValueError("Input correct date or weekday!")

        self.this = dt.datetime(y, m, d)
        self.weekday = self.this.isoweekday()

        curs.execute('SELECT * FROM homework WHERE date = ?', (self.this.date(),))

        if res := curs.fetchone():
            for i, v in ipairs(res):
                if i > 1:
                    self.homework.update([(i-1, v)])
        else:
            for i in Schedule.standart:
                self.homework.update([(i, None)])
    
    def getHomework(self, lessons = None):
        if lessons is None:
            lessons = Schedule.standart
        elif isinstance(lessons, int):
            lessons = [ lessons ]
        
        string = str()

        counter = 0
        for les in lessons:
            counter += 1
            if lesson := (self.homework).get(les, 'Нет данных'):
                string += lesson
            else:
                string += 'Нет данных'

            if counter < len(lessons):
                string += '\n'

        return string

