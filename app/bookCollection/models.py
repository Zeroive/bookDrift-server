from tools.db import DB
import time


class BOOKCOLLECTION(DB):

    def findonebylibraryId_bookId_id(self, userId=None, bookId=None, collectionId=None):
        if collectionId is not None:
            sql = "SELECT * FROM book_collection WHERE collectionId={}".format(collectionId)
        else:
            sql = "SELECT * FROM book_collection WHERE userId={} AND bookId={}".format(userId, bookId)

        return self.select_one(sql)

    def update(self, bookCollection):
        checkArray = ['newold', 'note', 'charge', 'driftTime']
        flag = True
        for i in checkArray:
            if bookCollection[i] is None or bookCollection[i] is '':
                flag = False
                break

        DBdate = self.findonebylibraryId_bookId_id(collectionId=bookCollection['collectionId'])

        if flag and DBdate['state'] == 0:
            bookCollection['state'] = 1

        sql = 'UPDATE book_collection SET num={}, state={}, newold="{}", note="{}", charge="{}", driftTime="{}" ' \
              'WHERE collectionId={};'\
            .format(bookCollection['num'], bookCollection['state'], bookCollection['newold'], bookCollection['note'],
                    bookCollection['charge'], bookCollection['driftTime'], bookCollection['collectionId'])
        self.inser_update_delete(sql)

    def insertOne(self, userId, bookId, num=1):
        sql = 'INSERT INTO book_collection(userId, bookId, state, num) VALUES ({}, {}, 1, {})'\
            .format(userId, bookId, num)
        self.inser_update_delete(sql)

    def findallbyuserid(self, userid):
        sql = 'SELECT collectionId, BC.bookId, num, newold, note, charge, driftTime, BC.createTime, bookName, ' \
              'thumbUrl, author, publishTime, publisher, price, BC.state ' \
              'FROM book_collection AS BC LEFT JOIN book_library AS BL ' \
              'ON BC.userId={} AND BC.bookId=BL.bookId'\
            .format(userid)
        return self.select_all(sql)
        pass


if __name__ == '__main__':
    # time_start = time.time()  # 记录开始时间
    # print(BOOKCOLLECTION().findallbyuserid(1))
    # time_end = time.time()  # 记录结束时间
    # time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    # print(time_sum)
    pass
