from tools.db import DB
import time


class BOOK(DB):

    def __init__(self):
        super().__init__()
        pass

    def __del__(self):
        self.db.close()
        pass

    def findbyISBN(self, isbn):
        sql = 'SELECT * FROM book_library WHERE isbn = {} LIMIT 0,1'.format(isbn)
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        # print(data)
        return data

    def countall(self):
        sql = 'select count(*) from book_library'
        print(self.select_one(sql))



if __name__ == '__main__':
    time_start = time.time()  # 记录开始时间
    BOOK().findbyISBN("9787560013473")
    # BOOK().countall()
    time_end = time.time()  # 记录结束时间
    time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    print(time_sum)
