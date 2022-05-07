from tools.db import DB


class USERLIBRARY(DB):

    def __init__(self):
        super().__init__()
        pass

    def __del__(self):
        self.db.close()
        pass

    def findbylibraryId_bookId_id(self, userId=None, bookId=None, collectionId=None):
        if id is not None:
            sql = "SELECT * FROM book_collection WHERE collectionId={}".format(collectionId)
        else:
            sql = "SELECT * FROM book_collection WHERE userId={} AND bookId={}".format(userId, bookId)
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        print(data)

    def findbyopenid(self, userId):
        sql = "SELECT * FROM user_library WHERE userId={}".format(userId)
        return self.select_all(sql)

    def update(self, bookCollection):
        sql = "UPDATE book_collection SET num={}, state={} WHERE libraryId={};"\
            .format(bookCollection['num'], bookCollection['state'], bookCollection['libraryId'])
        self.inser_update_delete(sql)

    def insertOne(self, userId, bookId, num=1):
        sql = 'INSERT INTO book_collection(userId, bookId, state, num) VALUES ({}, {}, 1, {})'\
            .format(userId, bookId, num)
        self.inser_update_delete(sql)


if __name__ == '__main__':
    # USERLIBRARY().findbylibraryId_bookId(id=3)
    # USERLIBRARY().update({
    #     'num': 2,
    #     'state': 1,
    #     'id': 3
    # })
    print(USERLIBRARY().findbyopenid(222))
    pass
