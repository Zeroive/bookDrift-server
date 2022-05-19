from tools.db import DB
from datetime import datetime


class DRIFTHISTORY(DB):
    def __init__(self):
        DB.__init__(self)
        self.table_name = 'drift_history'

    def insert_drift_history(self, driftid, lenderid, borrowerid):
        sql = 'INSERT INTO drift_history(driftId, lenderId, borrowerId) VALUES ({}, {}, {})'\
            .format(driftid, lenderid, borrowerid)
        return self.insert_update_delete(sql)


