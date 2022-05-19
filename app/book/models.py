from tools.db import DB
from app.recommendScore.models import RECOMMENDSCORE
import time


class BOOK(DB):

    def __init__(self):
        DB.__init__(self)
        self.table_name = 'book_library'

    def findbyISBN(self, isbn):
        sql = 'SELECT * FROM book_library WHERE isbn={} LIMIT 0,1'.format(isbn)
        # print(data)
        return self.select_one(sql)

    def find_by_bookid(self, bookid):
        sql = 'SELECT * FROM book_library WHERE bookId={}'.format(bookid)
        # print(data)
        return self.select_one(sql)

    def countall(self):
        sql = 'select count(*) from book_library'
        return self.select_one(sql)

    def find_by_bookid(self, bookid):
        sql = 'SELECT * FROM book_library WHERE bookId={}'.format(bookid)
        return self.select_one(sql)

    def find_all_like_bookname(self, bookname, limitfrom=0, limitto=20):
        sql = 'SELECT * FROM book_library WHERE bookName like "%{}%" LIMIT {}, {}'.format(bookname, limitfrom, limitto)
        return self.select_all(sql)


if __name__ == '__main__':
    time_start = time.time()  # 记录开始时间

    # print(BOOK().findbyISBN(9787307223950))
    testbook = BOOK().find_all_like_bookname('php')
    recom = RECOMMENDSCORE()
    for i in testbook:
        print(i['bookId'])
        recom.insert_one(5, i['bookId'], 5)
    time_end = time.time()  # 记录结束时间
    time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    print(time_sum)


# 2 java 3 python 4 c++
