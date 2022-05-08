from flask import Blueprint, request, Response
from io import BytesIO
import base64
from app.bookDrift.models import BOOKDRIFT
from app.user.models import USER
import json
import qrcode

bookDrift = Blueprint('bookDrift', __name__, url_prefix='/bookdrift')
bookDriftService = BOOKDRIFT()
userService = USER()


@bookDrift.route('/', methods=['POST'])
def index():
    return 'hello bookDrift'


@bookDrift.route('/insert', methods=['POST'])
def insert_drift_book():
    request_data = json.loads(request.get_data().decode('utf-8'))  # 将前端Json数据转为字典
    print(request_data)
    bookDriftService.insert(request_data['ownerId'], request_data['bookId'])

    record = bookDriftService.findbyowneridandbookId(request_data['ownerId'], request_data['bookId'])

    img = qrcode.make('/bookdrift/borrow?driftid='+str(record['driftId']))
    imgbyte = BytesIO()# 创建图片流
    img.save(imgbyte, format='PNG')
    imgbyte = imgbyte.getvalue()
    base64img = base64.b64encode(imgbyte)
    response_data = {
        'base64img': base64img.decode()# 解析为字符串，直接转换会有b' '
    }
    return json.dumps(response_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)
    # return Response(imgbyte, mimetype='image/png')  # 用自定义返回的数据及类型


@bookDrift.route('/borrow', methods=['POST'])
def borrow_drift_book():
    request_data = json.loads(request.get_data().decode('utf-8'))  # 将前端Json数据转为字典
    response_data = {}
    return json.dumps(response_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)


@bookDrift.route('/getbyuserid', methods=['POST'])
def get_book_drift_by_userid():
    request_data = json.loads(request.get_data().decode('utf-8'))  # 将前端Json数据转为字典
    response_data = {
        'driftBooksInfo': bookDriftService.find_by_lenderid(request_data['userId'])
    }
    return json.dumps(response_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)


