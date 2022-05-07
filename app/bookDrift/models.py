from tools.db import DB


class BOOKDRIFT(DB):

    def __init__(self):
        super().__init__()
        pass

    def __del__(self):
        self.db.close()
        pass

    def insert(self, ownerid, bookid):
        sql = 'INSERT INTO book_drift(ownerId, lenderId, bookId) VALUES ({}, {}, {})'\
            .format(ownerid, ownerid, bookid)
        self.inser_update_delete(sql)
        pass

    def findbyowneridandbookId(self, ownerid, bookid):
        sql = 'SELECT * FROM book_drift WHERE ownerId={} AND bookId={}'\
            .format(ownerid, bookid)
        return self.select_one(sql)


if __name__ == '__main__':
    print(BOOKDRIFT().findbyowneridandbookId(1, 525148))
