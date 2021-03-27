from .data import curs, con

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
