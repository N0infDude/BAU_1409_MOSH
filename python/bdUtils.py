# -*- coding: utf-8 -*-
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

    def insert_data(self, idRoute='', points='', countPoints='', time=''):
        """добавление в базу данных"""
        with self.connection:
            sql = """INSERT INTO routers(idRoute,points,countPoints,time)
                VALUES ('%(idRoute)s','%(points)s','%(countPoints)s','%(time)s');
                """ % {"idRoute": str(idRoute), "points": points, "countPoints": countPoints, "time": time}
            if debug == 1: print(sql)
            self.cursor.execute(sql)
            self.connection.commit()

    def select_all(self, table):
        """ Получаем все строки """
        with self.connection:
            return self.cursor.execute(f'SELECT * FROM {table}').fetchall()

    def select_single(self, rownum, table):
        """ Получаем одну строку с id rownum """
        with self.connection:
            if debug == 1: print('SQL ' + 'SELECT * FROM ' + table + ' WHERE id = ', rownum)
            return self.cursor.execute('SELECT * FROM ' + table + ' WHERE id = ?', (rownum,)).fetchall()[0]

    def count_rows(self, table):
        """ Считаем количество строк """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM ' + table).fetchall()
            return len(result)

    def select_routes(self, *points, time=0):
        """ Получаем все строки """
        sqlPoints = ""
        for p in points:
            sqlPoints += f' AND points REGEXP ".*{p}.*"'
        if debug == 1: print(f'SELECT * FROM routers WHERE time={time}{sqlPoints}')
        with self.connection:
            return self.cursor.execute(f'SELECT * FROM routers WHERE time={time}{sqlPoints}').fetchall()

    def select_route_with_end(self, points=[], time=0, countPoints=0):
        """ Получаем все строки """
        if 1 < int(countPoints) < 21:
            countPoints = f"AND countPoints={countPoints} "
        else:
            countPoints = ""
        if countPoints == "":
            if 0 < len(points) < 3:
                if len(points) == 2:
                    sql = f"""SELECT countPoints, COUNT(countPoints)
                                FROM routers WHERE time={time} AND points REGEXP ".*{points[0]}.*{points[1]}$"
                                GROUP BY countPoints
                            """
                else:
                    sql = f"""SELECT countPoints, COUNT(countPoints)
                                FROM routers WHERE time={time} AND points REGEXP ".*{points[0]}.*"
                                GROUP BY countPoints
                               """
                if debug == 1: print(sql)
                with self.connection:
                    return self.cursor.execute(sql).fetchall()

        if 0 < len(points) < 3:
            if len(points) == 2:
                sql = f'SELECT * from routers WHERE time={time} {countPoints}AND points REGEXP ".*{points[0]}.*{points[1]}$"'
            else:
                sql = f'SELECT * from routers WHERE time={time} {countPoints}AND points REGEXP ".*{points[0]}.*"'
            if debug == 1: print(sql)
            with self.connection:
                return self.cursor.execute(sql).fetchall()

        else:
            return None


    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()

