from flask import Blueprint, request
from app.userLibrary.models import USERLIBRARY
from app.user.models import USER
import json

userLibrary = Blueprint('userLibrary', __name__, url_prefix='/userLibrary')
userLibraryService = USERLIBRARY()
userService = USER()


@userLibrary.route('/')
def index():
    return "hello userLibrary"


# 从accessToken解析openid 找馆藏书籍
@userLibrary.route('/getbookcollection', methods=['POST'])
def getBookCollection():
    request_data = json.loads(request.get_data().decode('utf-8'))
    openid = request_data['accessToken'].split('-')[0]


@userLibrary.route('/addbookcollection', methods=['POST'])
def addbookcollection():
    request_data = json.loads(request.get_data().decode('utf-8'))
    print(request_data)
    openid = request_data['accessToken'].split('-')[0]
    print(openid)
    userid = userService.finduserbyopenid(openid)['userId']
    userLibraryService.insertOne(userid, request_data['bookId'])

    response_data = {}

    return json.dumps(response_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)


