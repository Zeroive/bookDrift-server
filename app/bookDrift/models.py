from tools.db import DB


class BOOKDRIFT(DB):

    def insert(self, ownerid, bookid):
        sql = 'INSERT INTO book_drift(ownerId, lenderId, bookId) VALUES ({}, {}, {})'\
            .format(ownerid, ownerid, bookid)
        self.insert_update_delete(sql)
        pass

    def findbyowneridandbookId(self, ownerid, bookid):
        sql = 'SELECT * FROM book_drift WHERE ownerId={} AND bookId={}'\
            .format(ownerid, bookid)
        return self.select_one(sql)

    def find_by_lenderid(self, lenderid):
        sql = 'SELECT driftId, collectionId, owerId, lenderId, newold, note, charge, driftTime, BC.createTime, bookName, ' \
              'thumbUrl, author, publishTime, publisher, price, BD.state ' \
              'FROM book_drift AS BD LEFT JOIN book_collection AS BC ' \
              'ON BD.lenderid={} AND BD.collectionId=BC.collectionId' \
              'LEFT JOIN book_library AS BL ON BC.bookId=BL.bookId'\
            .format(lenderid)

        return self.select_all(sql)


if __name__ == '__main__':
    print(BOOKDRIFT().findbyowneridandbookId(1, 525148))
    print()
    pass
