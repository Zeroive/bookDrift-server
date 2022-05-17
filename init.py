from flask import Flask
from app.user.views import user
from app.book.views import book
from app.userLibrary.views import userLibrary
from app.bookDrift.views import bookDrift
from app.bookCollection.views import bookCollection
from app.userCF.views import userCF

app = Flask(__name__)

app.register_blueprint(user)
app.register_blueprint(book)
app.register_blueprint(userLibrary)
app.register_blueprint(bookDrift)
app.register_blueprint(bookCollection)
app.register_blueprint(userCF)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
