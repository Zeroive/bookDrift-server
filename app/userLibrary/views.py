from flask import Blueprint, request
from app.userLibrary.models import USERLIBRARY
from app.user.models import USER
import json

userLibrary = Blueprint('userLibrary', __name__, url_prefix='/userlibrary')
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


@userLibrary.route('/getbyuserid', methods=['POST'])
def getuserlibrarybyuserid():
    request_data = json.loads(request.get_data().decode('utf-8'))
    response_data = userLibraryService.findbyuserid(request_data['userId'])

    return json.dumps(response_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)


@userLibrary.route('/update', methods=['POST'])
def updateuserlibraryinfo():
    request_data = json.loads(request.get_data().decode('utf-8'))
    userLibraryService.update(request_data)
    response_data = {}

    return json.dumps(response_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)
