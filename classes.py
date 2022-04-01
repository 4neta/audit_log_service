from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
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

class Person(db.Model):
    __tablename__ = 'people'

    person_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=20), nullable=False)
    surname = db.Column(db.String(length=30), nullable=False)
    login = db.Column(db.String(length=30), unique=True, nullable=False)
    hashpass = db.Column(db.String(length=40), nullable=False)
    charged = db.Column(db.Integer)
    phone = db.Column(db.Integer, unique=True, nullable=False)
    address = db.Column(db.String(length=100))
    is_admin = db.Column(db.Boolean)

    def __init__(self, person_id, name, surname, login, hashpass, charged, phone, address, is_admin):
        self.person_id = person_id
        self.name = name
        self.surname = surname
        self.login = login
        self.hashpass = hashpass
        self.charged = charged
        self.phone = phone
        self.address = address
        self.is_admin = is_admin

class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer)
    person_login = db.Column(db.String(length=30))
    price = db.Column(db.Integer)
    time = db.Column(db.String(length=30))

    def __init__(self, order_id, book_id, person_id, person_login, price, time):
        self.order_id = order_id
        self.book_id = book_id
        self.person_id = person_id
        self.person_login = person_login
        self.price = price
        self.time = time
        

class Audit(db.Model):
    __tablename__ = 'audit'

    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer)
    event = db.Column(db.String(length=50))
    time = db.Column(db.String(length=30))

    def __init__(self, log_id, person_id, event, time):
        self.log_id = log_id
        self.person_id = person_id
        self.event = event
        self.time = time