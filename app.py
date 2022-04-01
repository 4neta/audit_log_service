from classes import db, app, Person, Order, Book, Audit
from flask import Flask, render_template, request, session, g
from sqlalchemy import delete
from datetime import datetime
import sqlite3 as sql

currentuser = ""
now = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

def log(event):
    with sql.connect("data.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO audit (person_id, event, time) VALUES (?,?,?)", (currentuser, event, now))
        con.commit()

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
        currentuser = str(login)

    with sql.connect("data.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM people WHERE login = ? AND hashpass = ?", (login, hashpass))
        con.commit()

        if not cur.fetchone():
            log("Log in failure")
            return render_template("index.html", msg="Login failed")
        else:
            log("Log in success")
            return render_template("store.html", username=currentuser, books=Book.query.all(), people=Person.query.all())

@app.route("/signin", methods = ['POST','GET'])
def signin():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        newlogin = request.form['newlogin']
        newpass = request.form['newpass']
        phone = request.form['phone']
        address = request.form['address']
        hashpass = newpass
        global currentuser
        currentuser = str(newlogin)

        try:
            with sql.connect("data.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO people (name, surname, login, hashpass, charged, phone, address, is_admin) VALUES (?,?,?,?,?,?,?,?)", (name, surname, newlogin, hashpass, 0, phone, address, False) )
                con.commit()
                log("Sign in success")
                return render_template("store.html", books=Book.query.all(), username=newlogin)
        except:
            log("Sign in failure")
            con.rollback()
            return render_template("index.html", msg="Please try again")

@app.route("/adminlog", methods = ['POST', 'GET'])
def adminlog():
    if request.method == 'POST':
        adminlogin = request.form['adminlogin']
        adminpass = request.form['adminpass']
        adminhashpass = adminpass
        global currentuser
        currentuser = str(adminlogin)

        try:
            with sql.connect("data.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM people WHERE login = ? AND hashpass = ? AND is_admin = 1", (adminlogin, adminhashpass))
                con.commit()
                if not cur.fetchone():
                    log("Admin login attempt")
                    return render_template("index.html", msg="Login failed")
                else:
                    log("Admin login success")
                    return render_template("admin.html", adminlogin=currentuser, books=Book.query.all(), people=Person.query.all())
        except:
            log("Admin login failure")
            con.rollback()
            return render_template("index.html", msg="Please try again")

@app.route("/buy", methods = ['POST', 'GET'])
def buy():
    if request.method == 'POST':
        book_id = request.form['book_id']

        try:
            with sql.connect("data.db") as con:
                cur = con.cursor()
                cur.execute("SELECT quantity FROM books WHERE book_id = ?", (book_id,))
                con.commit()
                quantity = cur.fetchone()

                if not quantity:
                    con.rollback()
                    log("Book searching failure")
                    return render_template("store.html", msg="Book not found or unavailable", username=currentuser, books=Book.query.all(), people=Person.query.all())
                else:
                    newquantity = quantity[0] - 1
                    cur.execute("UPDATE books SET quantity = ? WHERE book_id = ?", (newquantity, book_id))
                    cur.execute("SELECT price FROM books WHERE book_id = ?", (book_id,))
                    price = cur.fetchone()

                    cur.execute("INSERT INTO orders (book_id, person_login, price, time) VALUES (?,?,?,?)", (book_id, currentuser, price[0], now))

                    cur.execute("SELECT charged FROM people WHERE login = ?", (currentuser,))
                    con.commit()
                    alreadycharged = cur.fetchone()
                    newcharge = alreadycharged[0] + price[0]

                    cur.execute("UPDATE people SET charged = ? WHERE login = ?", (newcharge, currentuser))
                    con.commit()
                    log("Book purchase success")
                    return render_template("store.html", username=currentuser, books=Book.query.all(), people=Person.query.all())
        except:
            log("Book purchase failure")
            con.rollback()
            return render_template("store.html", msg="Please try again", username=currentuser, books=Book.query.all(), people=Person.query.all())

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
                    log("Book searching attempt")
                    return render_template("admin.html", msg="Book not found", books=Book.query.all(), people=Person.query.all())
                else:
                    log("Update of a book's quantity")
                    return render_template("admin.html", msg="The quantity for this book has been updated", books=Book.query.all(), people=Person.query.all())
        except:
            log("Update of a book's quantity failure")
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
                    log("User removal attempt")
                    return render_template("admin.html", msg="Customer not found", books=Book.query.all(), people=Person.query.all())
                else:
                    cur.execute("DELETE FROM people WHERE person_id = ?", (person_id,))
                    con.commit()
                    log("User removal success")
                    return render_template("admin.html", msg="The account has been deleted", books=Book.query.all(), people=Person.query.all())
        except:
            con.rollback()
            log("User removal failure")
            return render_template("admin.html", msg="Please try again", books=Book.query.all(), people=Person.query.all())

@app.route("/showlog", methods = ['POST', 'GET'])
def showlog():
    if request.method == 'POST':
        person_id = request.form['id']
        choice = request.form['choice']

        if person_id:
            with sql.connect("data.db") as con:
                    cur = con.cursor()
                    cur.execute("SELECT login FROM people WHERE person_id = ?", (person_id,))
                    con.commit()
                    username = cur.fetchall()

            return render_template("admin.html", adminlogin=currentuser, books=Book.query.all(), people=Person.query.all(), logs=Audit.query.filter_by(person_id = username[0][0]).all())

        logs = Audit.query.all()
        msg=""

        if choice == '1':
            logs = Audit.query.filter((Audit.event == 'Sign in success') \
                                    | (Audit.event == 'Sign in failure'))
        elif choice == '2':
            logs = Audit.query.filter((Audit.event == 'Admin login attempt') \
                                    | (Audit.event == 'Admin login success') \
                                    | (Audit.event == 'Admin login failure') \
                                    | (Audit.event == 'Log in failure') \
                                    | (Audit.event == 'Log in success'))
        elif choice == '3':
            logs = Audit.query.filter((Audit.event == 'Book purchase success') \
                                    | (Audit.event == 'Book searching failure') \
                                    | (Audit.event == 'Book purchase failure') \
                                    | (Audit.event == "Update of a book's quantity") \
                                    | (Audit.event == "Update of a book's quantity failure"))
        elif choice == '4':
            logs = Audit.query.filter((Audit.event == 'User removal attempt') \
                                    | (Audit.event == 'User removal failure') \
                                    | (Audit.event == 'User removal success'))
        elif choice == '5':
            pass
        else:
            msg="There are only 4 types of events, please type a number from 1 to 5."
        return render_template("admin.html", adminlogin=currentuser, msg=msg, books=Book.query.all(), people=Person.query.all(), logs=logs)


app.run(debug=True, host="127.0.0.1", port=3000)