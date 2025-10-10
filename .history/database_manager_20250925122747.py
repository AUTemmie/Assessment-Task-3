import sqlite3 as sql
import os


class DBManager:
    def __init__(self):
        self.dbPath = os.path.join(os.getcwd(), "database", "data_source.db")

    def listExtension(self):
        con = sql.connect(self.dbPath)
        cur = con.cursor()
        data = cur.execute("SELECT * FROM extension").fetchall()
        con.close()
        return data

    def get_user_by_first_name(self, first_name):
        con = sql.connect(self.dbPath)
        cur = con.cursor()
        query = "SELECT first_name, password " "FROM users " "WHERE first_name=?"
        cur.execute(query, (first_name,))
        row = cur.fetchone()
        con.close()
        if row:
            return {"first_name": row[0], "password": row[1]}
        return None
