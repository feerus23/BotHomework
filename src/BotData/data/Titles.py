from .data import curs, con

class Title:
    'Класс для получения или изменения данных о званиях (приурочены к уровням доступа)'

    def Set(self, **levels):
        query = 'INSERT OR REPLACE INTO titles VALUES (?, ?)'

        for k, v in levels.items():
            curs.execute(query, (k, v))
        
        con.commit()

    def Get(self, permission):
        curs.execute('SELECT name FROM titles WHERE permission = ?', (permission,))

        if res := curs.fetchone():
            return res[0]
        else:
            return False
    
    def GetAll(self):
        curs.execute('SELECT * FROM titles')

        if res := curs.fetchall():
            return res
        else:
            return False
    
    def Del(self, *levels):
        query = 'DELETE FROM titles WHERE permission = ?'

        for v in levels:
            curs.execute(query, (v, ))
    
    def IsEmpty(self):
        curs.execute('SELECT * FROM titles')

        if curs.fetchone():
            return False
        else:
            return True
