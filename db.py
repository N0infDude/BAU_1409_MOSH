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