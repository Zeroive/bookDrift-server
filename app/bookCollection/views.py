from flask import Blueprint, request
import requests
import json
from app.bookCollection.models import BOOKCOLLECTION
from app.user.models import USER


bookCollection = Blueprint('bookCollection', __name__, url_prefix='/bookcollection')
bookCollectionService = BOOKCOLLECTION()
userService = USER()


@bookCollection.route('/', methods=['POST'])
def index():
    return 'hello bookcollection'


@bookCollection.route('/addbookcollection', methods=['POST'])
def addbookcollection():
    request_data = json.loads(request.get_data().decode('utf-8'))
    # openid = request_data['accessToken'].split('-')[0]
    # userid = userService.finduserbyopenid(openid)['userId']
    userid = request_data['userId']
    # 查看是否存在
    if bookCollectionService.find_by_userid_bookid(userid, request_data['bookId']):
        # 如果存在
        bookCollectionService.change_book_num_by_userid_bookid(userid, request_data['bookId'])
        pass
    else:
        # 否则新增
        bookCollectionService.insertOne(userid, request_data['bookId'])

    response_data = {}

    return json.dumps(response_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)


@bookCollection.route('/findallbyuserid', methods=['POST'])
def find_all_book_collection_by_userid():
    request_data = json.loads(request.get_data().decode('utf-8'))
    response_data = {
        'collectionBooksInfo': bookCollectionService.findallbyuserid(request_data['userId'])
    }
    # print(response_data)
    return json.dumps(response_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)


@bookCollection.route('/updatebycollectionid', methods=['POST'])
def update_book_collection_by_collectionid():
    request_data = json.loads(request.get_data().decode('utf-8'))
    # print(request_data)
    bookCollectionService.update(request_data)
    response_data = {}
    # print(response_data)
    return json.dumps(response_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)
    pass
