from enum import unique
from multiprocessing import AuthenticationError
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete
from datetime import datetime

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'


class Book(db.Model):
    __tablename__ = 'books'

    # TODO: Adjust parameters of columns
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

class Person(db.Model):
    __tablename__ = 'people'

    person_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=20))
    surname = db.Column(db.String(length=30))
    login = db.Column(db.String(length=30))
    hashpass = db.Column(db.String(length=40))
    charged = db.Column(db.Integer)
    phone = db.Column(db.Integer)
    is_admin = db.Column(db.Boolean)

    def __init__(self, person_id, name, surname, login, hashpass, charged, phone, is_admin):
        self.person_id = person_id
        self.name = name
        self.surname = surname
        self.login = login
        self.hashpass = hashpass
        self.charged = charged
        self.phone = phone
        self.is_admin = is_admin

class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer)
    person_id = db.Column(db.Integer)
    price = db.Column(db.Integer)
    time = db.Column(db.DateTime)

    def __init__(self, order_id, book_id, person_id, price, time):
        self.order_id = order_id
        self.book_id = book_id
        self.person_id = person_id
        self.price = price
        self.time = time


class Audit(db.Model):
    __tablename__ = 'audit'

    log_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer)
    event = db.Column(db.String(length=50))
    time = db.Column(db.DateTime)

    def __init__(self, log_id, person_id, event, time):
        self.log_id = log_id
        self.person_id = person_id
        self.event = event
        self.time = time

@app.route("/")
def show_login_page():
    return render_template("index.html", time=str(datetime.now()))

@app.route("/store/")
def show_books():
    return render_template("store.html", books=Book.query.all())

app.run(debug=True, host="127.0.0.1", port=3000)