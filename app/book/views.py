from flask import Blueprint, request
import requests
import json
from app.book.models import BOOK

book = Blueprint('book', __name__, url_prefix='/book')
bookService = BOOK()


@book.route('/')
def index():
    return "hello book"


@book.route('/findbook', methods=['POST'])
def findbook():
    request_data = json.loads(request.get_data().decode('utf-8'))
    bookInfo = BOOK().findbyISBN(request_data['isbn'])
    response_data = {'bookInfo': bookInfo}

    return json.dumps(response_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)


@book.route('/findbookbyname', methods=['POST'])
def find_book_by_name():
    request_data = json.loads(request.get_data().decode('utf-8'))
    print(request_data['bookName'])
    response_data = bookService.find_all_like_bookname(request_data['bookName'])
    return json.dumps(response_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)

@book.route('/findbybookid', methods=['POST'])
def find_by_bookid():
    request_data = json.loads(request.get_data().decode('utf-8'))
    response_data = bookService.find_by_bookid(request_data['bookId'])
    return json.dumps(response_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)
