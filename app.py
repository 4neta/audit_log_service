from enum import unique
from multiprocessing import AuthenticationError
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete
from datetime import datetime
import sqlite3 as sql

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

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

    def change_quantity(self, change):
        self.quantity += change

class Person(db.Model):
    __tablename__ = 'people'

    person_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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

    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer)
    event = db.Column(db.String(length=50))
    time = db.Column(db.DateTime)

    def __init__(self, log_id, person_id, event, time):
        self.log_id = log_id
        self.person_id = person_id
        self.event = event
        self.time = time

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        hashpass = password

        with sql.connect("data.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM people WHERE login = ? AND hashpass = ?", (login, hashpass))
            con.commit()
            if not cur.fetchone():
                return render_template("index.html", msg="Login failed")
            else:
                return render_template("store.html", username=login, books=Book.query.all(), people=Person.query.all())
            con.close()

@app.route("/signin", methods = ['POST','GET'])
def signin():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        newlogin = request.form['newlogin']
        newpass = request.form['newpass']
        phone = request.form['phone']
        hashpass = newpass

        try:
            with sql.connect("data.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO people (name, surname, login, hashpass, charged, phone, is_admin) VALUES (?,?,?,?,?,?,?)",(name,surname,newlogin,hashpass,0,phone,False) )
                con.commit()
                return render_template("store.html", books=Book.query.all())
        except:
            con.rollback()
            return render_template("index.html", msg="Please try again")
        con.close()

@app.route("/adminlog", methods = ['POST', 'GET'])
def adminlog():
    if request.method == 'POST':
        adminlogin = request.form['adminlogin']
        adminpass = request.form['adminpass']
        adminhashpass = adminpass

        try:
            with sql.connect("data.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM people WHERE login = '" + adminlogin + "' AND hashpass = '" + adminhashpass + "' AND is_admin = 1")
                con.commit()
                if not cur.fetchone():
                    return render_template("index.html", msg="Login failed")
                else:
                    return render_template("admin.html", adminlogin=adminlogin, books=Book.query.all(), people=Person.query.all())
                con.close()
        except:
            con.rollback()
            return render_template("index.html", msg="Please try again")

@app.route("/buy", methods = ['POST', 'GET'])
def buy():
    pass

@app.route("/updatequantity", methods = ['POST', 'GET'])
def updatequantity():
    if request.method == 'POST':
        book_id = request.form['book_id']
        add = request.form['add']
        try:
            with sql.connect("data.db") as con:
                cur = con.cursor()
                cur.execute("SELECT quantity FROM books WHERE book_id = ?", (book_id,))
                con.commit()
                quantity = cur.fetchall()[0][0]
                newquantity = int(quantity) + int(add)

                cur.execute("UPDATE books SET quantity = ? WHERE book_id = ?", (newquantity, book_id))
                con.commit()

                if not cur.fetchone():
                    return render_template("admin.html", msg="Book not found", books=Book.query.all(), people=Person.query.all())
                else:
                    return render_template("admin.html", msg="The quantity for this book has been updated", books=Book.query.all(), people=Person.query.all())
                con.close()
        except:
            con.rollback()
            return render_template("admin.html", msg="Please try again", books=Book.query.all(), people=Person.query.all())

@app.route("/deleteperson", methods = ['POST', 'GET'])
def deleteperson():
    pass

@app.route("/showlog", methods = ['POST', 'GET'])
def showlog():
    pass

app.run(debug=True, host="127.0.0.1", port=3000)

# TODO's:
# Could use the Flask-Login module instead of searching the database
