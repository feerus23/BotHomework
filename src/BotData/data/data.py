import sqlite3 as sql
import toml

tvar = toml.load('config.toml')['admins_id']; admin = []
for _, v in tvar.items(): admin.append(v)
del tvar

con = sql.connect('BotData\\data\\base\\base.sqlite')
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
                permission INT(2) NOT NULL PRIMARY KEY ON CONFLICT REPLACE,
                name CHAR(127) NOT NULL UNIQUE
            )'''
        ]

        for q in query: curs.execute(q)

        con.commit()

        return False
    else:
        return True
