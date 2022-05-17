from flask import Blueprint, request, Response
from io import BytesIO
import base64
from app.bookDrift.models import BOOKDRIFT
from app.user.models import USER
from app.bookCollection.models import BOOKCOLLECTION
import json
import qrcode

bookDrift = Blueprint('bookDrift', __name__, url_prefix='/bookdrift')
bookDriftService = BOOKDRIFT()
userService = USER()
bookCollectionService = BOOKCOLLECTION()


@bookDrift.route('/', methods=['POST'])
def index():
    return 'hello bookDrift'


# 添加在漂书籍
@bookDrift.route('/insert', methods=['POST'])
def insert_drift_book():
    request_data = json.loads(request.get_data().decode('utf-8'))  # 将前端Json数据转为字典
    print(request_data)
    collection_record = bookCollectionService.find_by_userid_bookid(request_data['ownerId'], request_data['bookId'])
    if not collection_record:
        # 表示未加入馆藏 加入馆藏
        bookCollectionService.insertOne(request_data['ownerId'], request_data['bookId'])
    else:
        # 存在馆藏 数量-1
        bookCollectionService.change_book_num_by_userid_bookid(request_data['ownerId'], request_data['bookId'], -1)
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
    print(driftid, borrowerid)
    bookDriftService.update_borrowerid_by_driftid(driftid, borrowerid, 1)
    response_data = {}
    return json.dumps(response_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)


# 根据userId获取在漂书籍
@bookDrift.route('/getbyuserid', methods=['POST'])
def get_book_drift_by_userid():
    request_data = json.loads(request.get_data().decode('utf-8'))  # 将前端Json数据转为字典
    response_data = {
        'driftBooksInfo': bookDriftService.find_by_lenderid(request_data['userId'])
    }
    return json.dumps(response_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)


# 查看放漂书籍详情
@bookDrift.route('/getdetail', methods=['POST'])
def get_book_drift_by_driftid():
    driftid = request.args.get('driftid', '')
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

