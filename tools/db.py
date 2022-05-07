import config
import pymysql
from pymysql.cursors import DictCursor


class DB:

    def __init__(self):
        self.db = pymysql.connect(**config.config, cursorclass=DictCursor)
        self.cursor = self.db.cursor()

    def inser_update_delete(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()

    def select_one(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def select_all(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()
