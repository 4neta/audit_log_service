from enum import unique
from multiprocessing import AuthenticationError
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(length=50))
    author = db.Column(db.String(length=30))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)

    def __init__(self, book_id, title, author, quantity, price):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.quantity = quantity
        self.price = price

    def change_quantity(self, change):
        self.quantity += change

@app.route("/")
def show_login_page():
    return render_template("index.html")

@app.route("/store/")
def show_books():
    return render_template("store.html", books=Book.query.all())

app.run(debug=True, host="127.0.0.1", port=3000)