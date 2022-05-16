import config
import pymysql
from pymysql.cursors import DictCursor


class DB:
    # db = pymysql.connect(**config.config, cursorclass=DictCursor)
    # cursor = db.cursor()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.db = pymysql.connect(**config.config, cursorclass=DictCursor)
        self.cursor = self.db.cursor()
        pass

    def __del__(self):
        try:
            self.db.close()
        except Exception as e:
            pass

    def insert_update_delete(self, sql):
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
