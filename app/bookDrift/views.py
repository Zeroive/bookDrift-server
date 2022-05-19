from flask import Blueprint, request, Response
from io import BytesIO
import base64
from app.bookDrift.models import BOOKDRIFT
from app.user.models import USER
from app.bookCollection.models import BOOKCOLLECTION
from app.driftHistory.models import DRIFTHISTORY
import json
import qrcode
import requests

bookDrift = Blueprint('bookDrift', __name__, url_prefix='/bookdrift')
bookDriftService = BOOKDRIFT()
userService = USER()
bookCollectionService = BOOKCOLLECTION()
driftHistoryService = DRIFTHISTORY()


@bookDrift.route('/', methods=['POST'])
def index():
    return 'hello bookDrift'


# 添加在漂书籍
@bookDrift.route('/insert', methods=['POST'])
def insert_drift_book():
    request_data = json.loads(request.get_data().decode('utf-8'))  # 将前端Json数据转为字典
    print(request_data)
    state = request_data.get('state')
    collection_record = bookCollectionService.find_by_userid_bookid(request_data['ownerId'], request_data['bookId'])
    if not collection_record:
        # 表示未加入馆藏 加入馆藏
        bookCollectionService.insertOne(request_data['ownerId'], request_data['bookId'])
    else:
        # 存在馆藏 数量-1
        # state 1 表示 是新增页面传来的 0 表示 个人页面传来的
        bookCollectionService.change_book_num_by_userid_bookid(request_data['ownerId'], request_data['bookId'],
                                                               (-1, 0)[state == 0])
    collection_record = bookCollectionService.find_by_userid_bookid(request_data['ownerId'], request_data['bookId'])
    # 插入book_drift
    bookDriftService.insert(collection_record['collectionId'], request_data['ownerId'])
    # 获得driftId
    drift_record = bookDriftService.find_by_ownerid_bookId(collection_record['collectionId'], request_data['ownerId'])

    # 二维码
    img = qrcode.make('/bookdrift/getdetail?driftid='+str(drift_record['driftId']))
    imgbyte = BytesIO()# 创建图片流
    img.save(imgbyte, format='PNG')
    imgbyte = imgbyte.getvalue()
    base64img = base64.b64encode(imgbyte)
    response_data = {
        'base64img': base64img.decode()# 解析为字符串，直接转换会有 b' '
    }
    return json.dumps(response_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)
    # return Response(imgbyte, mimetype='image/png')  # 用自定义返回的数据及类型


# 借入 改变书的状态 更新borrowerId
@bookDrift.route('/borrow', methods=['POST'])
def borrow_drift_book():
    request_data = json.loads(request.get_data().decode('utf-8'))  # 将前端Json数据转为字典
    borrowerid = request_data['userId']
    driftid = request_data['driftId']
    # print(driftid, borrowerid)

    # 根据 driftId 获取该放漂书籍
    driftbook = bookDriftService.find_by_driftid(driftid)
    if driftbook['lenderId'] == borrowerid:
        return {'msg': '无法捞起自己！'}, 400

    # 新增drift_history表
    drift_book = bookDriftService.find_by_driftid(driftid)
    driftHistoryService.insert_drift_history(drift_book['driftId'], drift_book['lenderId'], borrowerid)
    latest_history = driftHistoryService.select_latest_after_insert('historyId')
    # 更改book_drift表借入人和状态
    bookDriftService.update_borrowerid_by_driftid(driftid, borrowerid, 1, latest_history['historyId'])
    response_data = {}
    return json.dumps(response_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)


# 根据userId lenderId 在漂书籍
@bookDrift.route('/getbylenderid', methods=['POST'])
def get_book_drift_by_lenderid():
    request_data = json.loads(request.get_data().decode('utf-8'))  # 将前端Json数据转为字典

    books = bookDriftService.find_by_lenderid(request_data['lenderId'])
    # 检查url可用性
    for i in books:
        if requests.get(i['thumbUrl']).status_code == 200:
            i['isthumbUrlWork'] = True
        else:
            i['isthumbUrlWork'] = False
    response_data = {
        'driftBooksInfo': books
    }
    return json.dumps(response_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)


# 根据userId borrowerId 在漂书籍
@bookDrift.route('/getbyborrowerid', methods=['POST'])
def get_book_drift_by_borrowerid():
    request_data = json.loads(request.get_data().decode('utf-8'))  # 将前端Json数据转为字典

    books = bookDriftService.find_by_borrowerid(request_data['borrowerId'])
    # 检查url可用性
    for i in books:
        if requests.get(i['thumbUrl']).status_code == 200:
            i['isthumbUrlWork'] = True
        else:
            i['isthumbUrlWork'] = False
    response_data = {
        'pickedBooksInfo': books
    }
    return json.dumps(response_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)


# 查看放漂书籍详情
@bookDrift.route('/getdetail', methods=['POST', 'GET'])
def get_drift_book_detail_by_driftid():
    driftid = request.args.get('driftid', '')
    print(driftid)
    response_data = bookDriftService.find_driftbook_detail_by_driftid(driftid)
    return json.dumps(response_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)
    pass


# 根据driftid返回二维码
@bookDrift.route('/onemoredrift', methods=['POST'])
def get_drift_book_by_driftid():
    request_data = json.loads(request.get_data().decode('utf-8'))  # 将前端Json数据转为字典
    driftid = request_data['driftId']
    # 二维码
    img = qrcode.make('/bookdrift/getdetail?driftid=' + str(driftid))
    imgbyte = BytesIO()  # 创建图片流
    img.save(imgbyte, format='PNG')
    imgbyte = imgbyte.getvalue()
    base64img = base64.b64encode(imgbyte)
    response_data = {
        'base64img': base64img.decode()  # 解析为字符串，直接转换会有 b' '
    }
    return json.dumps(response_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)


# 根据userid返回 转漂记录
# 参数 userId
@bookDrift.route('/record', methods=['POST'])
def get_record_by_userid():
    request_data = json.loads(request.get_data().decode('utf-8'))  # 将前端Json数据转为字典

    books = bookDriftService.find_by_lenderid(request_data['userId']) + bookDriftService.find_by_borrowerid(request_data['userId'])
    # 倒序排序
    books.sort(key=lambda x: x['updateTime'], reverse=True)
    for i in books:
        i['date'] = i['updateTime'].strftime('%Y/%m/%d')
        i['time'] = i['updateTime'].strftime('%H:%M:%S')
    # 关键词截取
    keys = ['bookName', 'state', 'lenderId', 'borrowerId', 'driftId', 'date', 'time']
    books = [dict((key, i[key]) for key in keys) for i in books]
    response_data = books
    return json.dumps(response_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)

