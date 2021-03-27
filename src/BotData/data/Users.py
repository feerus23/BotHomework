from .data import checkDatabase, curs, con, admin

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
                    self.Prm.update([(1, 0), (2, '10б')])
                else:
                    self.Prm.update(self.__empty_list)
        else:
            if user_id in admin:
                self.Prm.update([(1, 0), (2, '10б')])
            else:
                self.Prm.update(self.__empty_list)

    def pSet(self, param, value):
        if type(param) == str:
            param = self.tparams[param]
        self.Prm[param] = value
    
    def pGet(self, param):
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
        columns = '(id, '; values = (); values_str = ' (?, '; cunt = 0

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
