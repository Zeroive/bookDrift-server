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
    print(request_data)
    openid = request_data['accessToken'].split('-')[0]
    print(openid)
    userid = userService.finduserbyopenid(openid)['userId']
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
