from tools.db import DB
from datetime import datetime


class BOOKDRIFT(DB):
    def __init__(self):
        DB.__init__(self)
        self.table_name = 'book_drift'

    def insert(self, collectionid, lenderid, borrowerid=-1, state=0):
        sql = 'INSERT INTO book_drift(collectionId, lenderId, borrowerId, state) VALUES ({}, {}, {}, {})' \
            .format(collectionid, lenderid, borrowerid, state)
        self.insert_update_delete(sql)
        pass

    def find_by_ownerid_bookId(self, collectionid, lenderid, borrowerid=-1):
        sql = 'SELECT * FROM book_drift WHERE collectionId={} AND lenderId={} AND borrowerId={}' \
            .format(collectionid, lenderid, borrowerid)
        return self.select_one(sql)

    def find_by_driftid(self, driftid):
        sql = 'SELECT * FROM book_drift WHERE driftId={}'.format(driftid)
        return self.select_one(sql)

    def find_by_lenderid(self, lenderid):
        sql = 'SELECT driftId, BD.collectionId, lenderId, borrowerId, newold, note, num, charge, driftTime, ' \
              'BD.updateTime, bookName, thumbUrl, author, publishTime, publisher, price, BD.state, BD.createTime ' \
              'FROM book_drift AS BD LEFT JOIN book_collection AS BC ' \
              'ON BD.collectionId=BC.collectionId ' \
              'LEFT JOIN book_library AS BL ON BC.bookId=BL.bookId ' \
              'WHERE BD.lenderId={}' \
            .format(lenderid)
        return self.select_all(sql)

    def find_by_borrowerid(self, borrowerid):
        sql = 'SELECT driftId, BD.collectionId, lenderId, borrowerId, newold, note, num, charge, driftTime, price, ' \
              'BD.updateTime, BD.createTime, bookName, thumbUrl, author, publishTime, publisher,  BD.state, BC.bookId ' \
              'FROM book_drift AS BD LEFT JOIN book_collection AS BC ' \
              'ON BD.collectionId=BC.collectionId ' \
              'LEFT JOIN book_library AS BL ON BC.bookId=BL.bookId ' \
              'WHERE BD.borrowerId={}' \
            .format(borrowerid)
        return self.select_all(sql)

    def update_borrowerid_by_driftid(self, driftid, borrowerid, state, historyid):
        sql = 'UPDATE book_drift SET borrowerId={},state={},historyId={} WHERE driftId={}'\
            .format(borrowerid, state, historyid, driftid)
        self.insert_update_delete(sql)

    def find_driftbook_detail_by_driftid(self, driftid):
        sql = 'SELECT driftId, BD.createTime, BD.state, lenderId, borrowerId, BC.userId ownerId, BC.bookId,' \
              'BC.newold, BC.note, BC.charge, BC.driftTime, UI1.nickName lenderName, UI1.avatarUrl lenderAvatarUrl,' \
              'UI2.nickName borrowerName, UI2.avatarUrl borrowerAvatarUrl, bookName, thumbUrl, author, publisher,' \
              'price, UI2.avatarUrl borrowerAvatarUrl, libraryName ' \
              'FROM book_drift as BD ' \
              'JOIN book_collection AS BC ON BD.collectionId=BC.collectionId ' \
              'JOIN user_info AS UI1 ON BD.lenderId = UI1.userId ' \
              'JOIN user_info AS UI2 ON BD.borrowerId = UI2.userId ' \
              'JOIN book_library AS BL ON BC.bookId=BL.bookId ' \
              'JOIN user_library AS UL ON BC.libraryId=UL.libraryId ' \
              'WHERE BD.driftId={}'.format(driftid)
        return self.select_one(sql)
        pass



if __name__ == '__main__':
    BD = BOOKDRIFT()
    # print(BOOKDRIFT().findbyowneridandbookId(1, 525148))
    # print(BOOKDRIFT().find_by_lenderid(1))
    # BOOKDRIFT().update_borrowerid_by_driftid(2, 1)
    # print(BOOKDRIFT().find_driftbook_detail_by_driftid(5))
    # books = BD.find_by_lenderid(1) + BD.find_by_borrowerid(1)
    # books.sort(key=lambda x: x['updateTime'], reverse=True)
    # for i in books:
    #     i['date'] = i['updateTime'].strftime('%Y-%m-%d')
    #     i['time'] = i['updateTime'].strftime('%H:%M:%S')
    # keys = ['bookName', 'state', 'lenderId', 'borrowerId', 'driftId', 'date', 'time']
    # books = [dict((key, i[key]) for key in keys) for i in books]
    # print(books)
    pass

# {
#  'driftId': 5, 'collectionId': 18, 'lenderId': 1, 'borrowerId': -1, 'state': 0,
#  'createTime': datetime.datetime(2022, 5, 7, 23, 10, 1), 'updateTime': datetime.datetime(2022, 5, 12, 10, 39, 26),
#  'BC.collectionId': 18, 'userId': 1, 'bookId': 9, 'num': 1, 'newold': None, 'note': None, 'charge': None,
#  'driftTime': None, 'BC.state': 2, 'BC.createTime': datetime.datetime(2022, 5, 12, 9, 54, 24),
#  'BC.updateTime': datetime.datetime(2022, 5, 12, 10, 51, 23), 'UI1.userId': 1, 'openId': 'og6Wu5D7G0nM3SXQ0P2kE6WIKLJs',
#  'sessionKey': '0LlKLnTZQ5nAJf6WEzCKZQ==', 'nickName': '???????????????\uf8ff???????????????',
#  'avatarUrl': 'https://thirdwx.qlogo.cn/mmopen/vi_32/8O7wCx1X6Whpk5CWDmyUstgJCicHTOn2MfHy6nvAR6FchO0ib9onlQwibKlTMDzB2icDvdI10bqSiaqRibnqMgFBMziaw/132',
#  'city': '', 'gender': '0', 'province': '', 'district': '', 'language': 'zh_CN', 'addressCode': None, 'latitude': None,
#  'longitude': None, 'UI2.userId': -1, 'UI2.openId': '0', 'UI2.sessionKey': '0', 'UI2.nickName': None,
#  'UI2.avatarUrl': None, 'UI2.city': None, 'UI2.gender': None, 'UI2.province': None, 'UI2.district': None,
#  'UI2.language': None, 'UI2.addressCode': None, 'UI2.latitude': None, 'UI2.longitude': None, 'BL.bookId': 9,
#  'bookName': '????????????', 'isbn': '9787568220958', 'thumbUrl': 'http://image12.bookschina.com/2016/20161003/s7280431.jpg',
#  'author': '????????????', 'kinder': None,
#  'memo': '????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????zui???????????????????????????',
#  'isbnJson': None, 'publishTime': '2016-06-01', 'publisher': '???????????????????????????', 'sellPrice': '17.0', 'price': '25.0',
#  'discount': '6.8???', 'BL.state': 1, 'BL.createTime': datetime.datetime(2019, 7, 9, 17, 11, 15), 'BL.updateTime': None
#  }
