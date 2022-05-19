from tools.db import DB
import time


class BOOKCOLLECTION(DB):
    def __init__(self):
        DB.__init__(self)
        self.table_name = 'book_collection'

    def find_by_userid_bookid(self, userid, bookid):
        sql = "SELECT * FROM book_collection WHERE userId={} AND bookId={}".format(userid, bookid)
        return self.select_one(sql)

    def find_by_collectionid(self, collectionid):
        sql = "SELECT * FROM book_collection WHERE collectionId={}".format(collectionid)
        return self.select_one(sql)

    def update(self, bookCollection):
        # 判断四个条件是否设置
        checkArray = ['newold', 'note', 'charge', 'driftTime']
        flag = True
        for i in checkArray:
            if bookCollection[i] is None or bookCollection[i] is '':
                flag = False
                break

        DBdate = self.find_by_collectionid(bookCollection['collectionId'])

        if flag and DBdate['state'] == 0:
            bookCollection['state'] = 1

        sql = 'UPDATE book_collection SET num={}, state={}, newold="{}", note="{}", charge="{}", driftTime="{}" ' \
              'WHERE collectionId={};' \
            .format(bookCollection['num'], bookCollection['state'], bookCollection['newold'], bookCollection['note'],
                    bookCollection['charge'], bookCollection['driftTime'], bookCollection['collectionId'])
        self.insert_update_delete(sql)

    def insertOne(self, userid, bookid, num=0, state=0):
        sql = 'INSERT INTO book_collection(userId, bookId, state, num) ' \
              'VALUES ({}, {}, {}, {})' \
            .format(userid, bookid, state, num)
        self.insert_update_delete(sql)

    def findallbyuserid(self, userid):
        sql = 'SELECT collectionId, BC.bookId, num, newold, note, charge, driftTime, BC.createTime, bookName, ' \
              'thumbUrl, author, publishTime, publisher, price, BC.state ' \
              'FROM book_collection AS BC LEFT JOIN book_library AS BL ' \
              'ON BC.bookId=BL.bookId ' \
              'WHERE BC.userId={}' \
            .format(userid)
        return self.select_all(sql)
        pass

    def update_state_by_collectionid(self, state, collectionid):
        sql = 'UPDATE book_collection SET state={} WHERE collectionId={}'.format(state, collectionid)
        self.insert_update_delete(sql)

    def change_book_num_by_userid_bookid(self, userid, bookid, num=1):
        sql = 'UPDATE book_collection SET num={} WHERE userId={} AND bookId={}'.format('num+0'+str(num), userid, bookid)
        self.insert_update_delete(sql)

    def find_collectionbook_detail_by_collectionid(self, collectionid):
        sql = 'SELECT bookName, thumbUrl, author, publisher, price, BC.newold, BC.note, BC.charge, BC.driftTime, ' \
              'UI.nickName lenderName, UI.avatarUrl lenderAvatarUrl, libraryName ' \
              'FROM book_collection AS BC ' \
              'JOIN user_info AS UI ON BC.userId=UI.userId ' \
              'JOIN book_library AS BL ON BC.bookId=BL.bookId ' \
              'JOIN user_library AS UL ON BC.libraryId=UL.libraryId ' \
              'WHERE collectionId={}'.format(collectionid)

        return self.select_one(sql)


if __name__ == '__main__':
    # time_start = time.time()  # 记录开始时间
    # print(BOOKCOLLECTION().findallbyuserid(1))
    # time_end = time.time()  # 记录结束时间
    # time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    # print(time_sum)
    # print(BOOKCOLLECTION().find_by_collectionid(2))
    # BOOKCOLLECTION().change_book_num_by_userid_bookid(1, 25, 10)
    print(BOOKCOLLECTION().find_collectionbook_detail_by_collectionid(5))
    pass
