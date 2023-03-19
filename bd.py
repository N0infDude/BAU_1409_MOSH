import sqlite3
import re

from config import debug


class SQLighter:

    def regexp(self, expr, item):
        reg = re.compile(expr)
        return reg.search(item) is not None

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self.connection.create_function("REGEXP", 2, self.regexp)

    def insert_data(self, id='', s='', SHcount=''):
        """добавление в базу данных"""
        with self.connection:
            sql = """INSERT INTO routers(id,S,SHcount)
                VALUES ('%(id)s','%(S)s','%(SHcount)s');
                """ % {"id": str(id), "S": S, "SHcount": SHcount}
            if debug == 1: print(sql)
            self.cursor.execute(sql)
            self.connection.commit()
