from tools.db import DB


class USERLIBRARY(DB):

    def findbyuserid(self, userId):
        sql = "SELECT * FROM user_library WHERE userId={}".format(userId)
        return self.select_one(sql)

    def update(self, libraryInfo):
        sql = 'UPDATE user_library SET libraryName="{}", longitude={}, latitude={}, introduction="{}", phone="{}", ' \
              'detailAddress="{}", province="{}", city="{}", district="{}" WHERE libraryId={}'\
            .format(libraryInfo['libraryName'], libraryInfo['longitude'], libraryInfo['latitude'], libraryInfo['introduction'],
                    libraryInfo['phone'], libraryInfo['detailAddress'], libraryInfo['province'], libraryInfo['city'],
                    libraryInfo['district'], libraryInfo['libraryId'])
        self.inser_update_delete(sql)
        pass


if __name__ == '__main__':
    # USERLIBRARY().findbylibraryId_bookId(id=3)
    # USERLIBRARY().update({
    #     'num': 2,
    #     'state': 1,
    #     'id': 3
    # })
    print(USERLIBRARY().findbyopenid(222))
    pass
