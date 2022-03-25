from email.policy import default
import random
from turtle import title
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "books.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class book (db.Model) :
    Title = db.Column(db.String(80), nullable=False, primary_key=True)
    Author = db.Column(db.String(80), nullable=False)
    Year = db.Column(db.Integer, nullable=False)
    Link = db.Column(db.String(80), nullable= True)
    Read = db.Column(db.Boolean, default=False)
    dateAdded = db.Column(db.DateTime, default=datetime.now)

def add_book (Title, Author, Year, Link) :
    if db.session.query(book).filter_by(Title = Title).first() is None : 
        bk = book(Title=Title, Author=Author, Year=Year, Link=Link)
        db.session.add(bk)
        db.session.commit()
        db.session.refresh(bk)
    else : 
        "book already exists"


def update_book (title, author, year, link , read) :
    db.session.query(book).filter_by(Title=title).update(
       {"Author":author, "Year":year, "Link":link, "Read": True if read == "on" else False})
    
    db.session.commit()

def mark_read (title) :
    db.session.query(book).filter_by(Title=title).update(
       {"Read": True})
    db.session.commit()
    
def get_all_books () :
    return db.session.query(book).all()

def get_books_read () :
    return db.session.query(book).filter_by(Read=True).all()
    
def get_books_unread () :
    return db.session.query(book).filter_by(Read=False).all()

def delete_book (Title) :
    bk = db.session.query(book).filter_by(Title=Title).first()
    db.session.delete(bk)
    db.session.commit()

def reset_list () :
   db.session.query(book).delete()
   db.session.commit()


@app.route("/" , methods=["GET", "POST"])

def view_index() :
    if request.method == "POST" :
       add_book(request.form["Title"], request.form["Author"], request.form["Year"], request.form["Link"])
    return render_template("index.html", books_read = get_books_read(), books_unread = get_books_unread())


@app.route ("/update/<book_title>", methods=["POST", "GET"])
def update_book_page(book_title) :
    if request.method == "POST" :
        mark_read(book_title)
    elif request.method == "GET" :
        delete_book(book_title)
    return redirect ("/" , code = 302)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=False)
    
    
    
   





    
