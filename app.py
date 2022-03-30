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

    # TODO: Adjust parameters of columns
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
    name = db.Column(db.String(length=20))
    surname = db.Column(db.String(length=30))
    login = db.Column(db.String(length=30), unique=True)
    hashpass = db.Column(db.String(length=40))
    charged = db.Column(db.Integer)
    phone = db.Column(db.Integer, unique=True)
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
    time = db.Column(db.DateTime)

    def __init__(self, log_id, person_id, event, time):
        self.log_id = log_id
        self.person_id = person_id
        self.event = event
        self.time = time

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

currentuser = ""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        hashpass = password
        global currentuser
        currentuser = login

    with sql.connect("data.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM people WHERE login = ? AND hashpass = ?", (login, hashpass))
        con.commit()
        if not cur.fetchone():
            return render_template("index.html", msg="Login failed")
        else:
            currentuser = login
            return render_template("store.html", username=login, books=Book.query.all(), people=Person.query.all())

@app.route("/signin", methods = ['POST','GET'])
def signin():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        newlogin = request.form['newlogin']
        newpass = request.form['newpass']
        phone = request.form['phone']
        hashpass = newpass
        global currentuser
        currentuser = newlogin

        try:
            with sql.connect("data.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO people (name, surname, login, hashpass, charged, phone, is_admin) VALUES (?,?,?,?,?,?,?)",(name,surname,newlogin,hashpass,0,phone,False) )
                con.commit()
                currentuser = newlogin
                return render_template("store.html", books=Book.query.all(), username=newlogin)
        except:
            con.rollback()
            return render_template("index.html", msg="Please try again")

@app.route("/adminlog", methods = ['POST', 'GET'])
def adminlog():
    if request.method == 'POST':
        adminlogin = request.form['adminlogin']
        adminpass = request.form['adminpass']
        adminhashpass = adminpass
        global currentuser
        currentuser = adminlogin

        try:
            with sql.connect("data.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM people WHERE login = ? AND hashpass = ? AND is_admin = 1", (adminlogin, adminhashpass))
                con.commit()
                if not cur.fetchone():
                    return render_template("index.html", msg="Login failed")
                else:
                    currentuser = adminlogin
                    return render_template("admin.html", adminlogin=adminlogin, books=Book.query.all(), people=Person.query.all())
        except:
            con.rollback()
            return render_template("index.html", msg="Please try again")

@app.route("/buy", methods = ['POST', 'GET'])
def buy():
    if request.method == 'POST':
        book_id = request.form['book_id']

        now = datetime.now()
        strnow = now.strftime("%d/%m/%Y %H:%M:%S")

        try:
            with sql.connect("data.db") as con:
                cur = con.cursor()
                cur.execute("SELECT quantity FROM books WHERE book_id = ?", (book_id,))
                con.commit()
                quantity = cur.fetchone()
                if not quantity:
                    return render_template("store.html", msg="Book not found or unavailable", books=Book.query.all())
                else:
                    newquantity = quantity[0] - 1
                    cur.execute("UPDATE books SET quantity = ? WHERE book_id = ?", (newquantity, book_id))
                    cur.execute("SELECT price FROM books WHERE book_id = ?", (book_id,))
                    price = cur.fetchone()
                    cur.execute("INSERT INTO orders (book_id, person_id, person_login, price, time) VALUES (?,?,?,?,?)", (book_id, 1, currentuser, price[0], strnow))
                    con.commit()
                    return render_template("store.html", username=currentuser, books=Book.query.all())
        except:
            con.rollback()
            return render_template("store.html", msg="Please try again", books=Book.query.all())

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
        except:
            con.rollback()
            return render_template("admin.html", msg="Please try again", books=Book.query.all(), people=Person.query.all())

@app.route("/deleteperson", methods = ['POST', 'GET'])
def deleteperson():
    if request.method == 'POST':
        person_id = request.form['person_id']
        try:
            with sql.connect("data.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM people WHERE person_id = ?", (person_id,))
                con.commit()
                if not cur.fetchone():
                    return render_template("admin.html", msg="Customer not found", books=Book.query.all(), people=Person.query.all())
                else:
                    cur.execute("DELETE FROM people WHERE person_id = ?", (person_id,))
                    con.commit()
                    return render_template("admin.html", msg="The account has been deleted", books=Book.query.all(), people=Person.query.all())
        except:
            con.rollback()
            return render_template("admin.html", msg="Please try again", books=Book.query.all(), people=Person.query.all())

@app.route("/showlog", methods = ['POST', 'GET'])
def showlog():
    pass

app.run(debug=True, host="127.0.0.1", port=3000)

# TODO's:
# Use the Flask-Login module instead of searching the database
# Greetings with name, not the username
# Let the user change his password or deactivate his account
# Introduce admins administration - super admin role