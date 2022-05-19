from flask import Blueprint, request
from app.remark.models import REMARK
from app.bookDrift.models import BOOKDRIFT
import json


remark = Blueprint('remark', __name__, url_prefix="/remark")
remarkService = REMARK()
bookDriftService = BOOKDRIFT()


@remark.route('/findbydriftid', methods=['POST'])
def find_by_driftid():
    request_data = json.loads(request.get_data().decode('utf-8'))  # 将前端Json数据转为字典
    remarks = remarkService.find_by_driftid(request_data['driftId'])
    # 倒序排序
    remarks.sort(key=lambda x: x['updateTime'], reverse=True)
    for i in remarks:
        i['date'] = i['updateTime'].strftime('%Y/%m/%d')
        i['time'] = i['updateTime'].strftime('%H:%M:%S')
    response_data = remarks
    return json.dumps(response_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)


@remark.route('/add', methods=['POST'])
def add_by_driftid():
    request_data = json.loads(request.get_data().decode('utf-8'))  # 将前端Json数据转为字典
    driftid = request_data['driftId']
    memo = request_data['memo']
    historyid = bookDriftService.find_by_driftid(driftid)['historyId']
    remarkService.insert_one(historyid, memo)
    response_data = {}
    return json.dumps(response_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)
