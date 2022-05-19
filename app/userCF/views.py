from flask import Blueprint, request
from app.userCF.models import RECOMMENDER
from app.book.models import BOOK
import json


userCF = Blueprint('userCF', __name__, url_prefix="/userCF")
UserRecommendService = RECOMMENDER()
bookService = BOOK()


@userCF.route('/')
def index():
    return "helleo userCF"


@userCF.route('/recommend', methods=['POST'])
def recommend_by_userid():
    request_data = json.loads(request.get_data().decode('utf-8'))  # 将前端Json数据转为字典
    bookidlist = UserRecommendService.recommend(request_data['userId'])
    num = request_data['num']
    booklist = []
    for i in bookidlist:
        booklist.append(bookService.find_by_bookid(i[0]))
    response_data = booklist[:num]
    return json.dumps(response_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)

