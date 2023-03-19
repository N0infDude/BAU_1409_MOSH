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

    def insert_data_routers(self, case='', S='', SHcount=''):
        """добавление в базу данных"""
        with self.connection:
            sql = """INSERT INTO routers(case,S,SHcount)
                VALUES ('%(case)s','%(S)s','%(SHcount)s');
                """ % {"case": case, "S": S, "SHcount": SHcount}
            if debug == 1: print(sql)
            self.cursor.execute(sql)
            self.connection.commit()

    def insert_data_cases(self, NameCase=''):
        """добавление в базу данных"""
        with self.connection:
            sql = """INSERT INTO Cases(NameCase)
                VALUES ('%(NameCase)s');
                """ % {"NameCase": NameCase}
            if debug == 1: print(sql)
            self.cursor.execute(sql)
            self.connection.commit()

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()