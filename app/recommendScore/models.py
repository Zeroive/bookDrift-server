from tools.db import DB


class RECOMMENDSCORE(DB):
    def __init__(self):
        DB.__init__(self)
        self.table_name = 'recommend_score'

    def find_all(self):
        sql = 'SELECT * FROM recommend_score'
        return self.select_all(sql)

    def insert_one(self, userid, bookid, score):
        sql = 'INSERT INTO recommend_score VALUES ({}, {}, {})'.format(userid, bookid, score)
        return self.insert_update_delete(sql)


if __name__ == "__main__":
    RR = RECOMMENDSCORE()
    for i in range(2, 12):
        print(i)
        # RR.insert_one(1, 1, 5)
    pass
