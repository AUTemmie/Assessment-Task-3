import sqlite3 as sql
import os


class DBManager:
    def __init__(self):
        self.dbPath = os.path.join(os.getcwd(), 'database', 'data_source.db')


def listExtension():
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    data = cur.execute('SELECT * FROM extension').fetchall()
    con.close()
    return data
