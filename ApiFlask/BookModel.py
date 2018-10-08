from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from settings import app
from collections import OrderedDict

db = SQLAlchemy(app)

class Book(db.Model):
 id = db.Column('book_id', db.Integer, primary_key = True)
 name = db.Column(db.String(100))
 price = db.Column(db.Float,nullable=False)  
 isbn = db.Column(db.Integer,nullable=False)
 
def add_book(_name,_price,_isbn):
    new_book=Book(name=_name,price=_price,isbn=_isbn)
    db.session.add(new_book)
    db.session.commit()
    
def delete_book(_isbn):
    deleting_book = {}
    deleting_book =Book.query.filter_by(isbn = _isbn).first()
    if (deleting_book != {}): 
        db.session.delete(deleting_book)
        db.session.commit()
        return "True"
    else:
        return "False"

def replace_book(_isbn,_name,_price):
    updating_book= {}
    updating_book= Book.query.filter_by(isbn=_isbn).first()
    if (updating_book != {}): 
        updating_book.isbn=_isbn
        updating_book.name=_name
        updating_book.price=_price
        db.session.commit()
        return "True"
    else:
        return "False"

def update_book(_isbn,_column,_newValue):
    updating_book={}
    updating_book =Book.query.filter_by(isbn=_isbn).first()
    if (updating_book != {}):
        if(_column == "isbn"):  
            updating_book.isbn = _newValue
        if(_column =="name"):  
            updating_book.name = _newValue
        if(_column == "price"):  
            updating_book.price = _newValue
        db.session.commit()
        return "True"
    else:
        return "False"
    
def get_all_books():
    allbooks = Book.query.all()
    result= []
    for b in allbooks:
        result.insert(0,Serialze(b))
    return result

def get_book_byisbn(_isbn):
    findbook= Book.query.filter_by(isbn=_isbn).first()
    return Serialze(findbook)


def Serialze(self):
    return ({"isbn": self.isbn,"name":self.name,"price":self.price})

#db.create_all()


