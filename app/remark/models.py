from tools.db import DB


class REMARK(DB):
    def __init__(self):
        DB.__init__(self)
        self.table_name = 'uesr_remark'

    # 先从drift_history中找出driftId对应的historyId
    # 再用 historyId 从 user_remark 中找出
    def find_by_driftid(self, driftid):
        sql = 'SELECT DH.historyId, memo, UR.updateTime, UI1.nickName lenderName, UI2.nickName borrowerName ' \
              'FROM drift_history as DH ' \
              'JOIN user_remark as UR ON DH.historyId=UR.historyId ' \
              'JOIN user_info as UI1 ON DH.lenderId=UI1.userId ' \
              'JOIN user_info as UI2 ON DH.borrowerId=UI2.userId ' \
              'WHERE DH.driftId={}'.format(driftid)
        return self.select_all(sql)
    # {'historyId': 1, 'driftId': 52, 'lenderId': 2, 'borrowerId': 1, 'createTime': datetime.datetime(2022, 5, 19,
    # 16, 34, 3), 'remarkId': 1, 'UR.historyId': 1, 'memo': '123321', 'UR.createTime': datetime.datetime(2022, 5, 19,
    # 19, 38, 47), 'updateTime': datetime.datetime(2022, 5, 19, 19, 38, 47)

    def insert_one(self, historyid, memo):
        sql = 'INSERT INTO user_remark(historyId, memo) VALUES ({}, "{}")'.format(historyid, memo)
        return self.insert_update_delete(sql)

if __name__ == '__main__':
    remark = REMARK()
    print(remark.find_by_driftid(52))