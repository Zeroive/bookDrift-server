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
