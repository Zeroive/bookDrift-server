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



