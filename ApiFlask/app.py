from flask import Flask , jsonify , request , Response 
import json
from settings import *



books = [
    {
        'name' : 'Green Eggs and Ham',
        'price': 7.99,
        'isbn' : 9871
    },
     {
        'name' : 'open your main',
        'price': 8.99,
        'isbn' : 9872
    }
]


@app.route('/')
def hello_to_myapi():
    return 'Hello to My Api Rest with Flask'

@app.route('/books')

def get_books():
    return jsonify ({'books':books})



@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value ={}
    for book in books :
        if book["isbn"] == isbn :
            return_value = book
    return jsonify (return_value)

def check_book(book):
    if ("name" in book and "price" in book and "isbn" in book):
        return "True"
    else : 
        return "False"


@app.route('/books',methods=['POST'])
def add_book():
    data = request.get_json()
    if (check_book(data)== "True"):
        books.insert(0,data)
        response = Response("",201,mimetype='application/json')
        response.headers['Location'] = '/books/' + str (data["isbn"])
        return response
    else: 
        errorInvalidObjectMessage = {
            "error" : "invalid book object passed in request",
            "helpString": "object should be similar to {'name': 'bookname', 'price': 'bookprice' , 'isbn' : 'bookisbn'}"
        }
        response = Response(json.dumps(errorInvalidObjectMessage),400,mimetype='application/json')
        return response

@app.route('/books/<int:isbn>', methods=['PUT'])
def Replacebook(isbn):
    if (get_book_by_isbn(isbn) != {}):
        data = request.get_json()
        upBook = {
            "name" : data["name"],
            "price" : data["price"],
            "isbn" : isbn
        }
        updateBooks(upBook)
        response = Response("",status=204)
        response.headers['Location'] = '/books/' + str (isbn)
        return response
    else :
        errorInvalidObjectMessage = {
            "error" : "book not found"
        }
        response = Response(json.dumps(errorInvalidObjectMessage),400,mimetype='application/json')
        return response

def updateBooks(newbook):
    for book in books:
        if newbook["isbn"] == book["isbn"]:
            book["name"] = newbook["name"]
            book["price"] = newbook["price"]

@app.route('/books/<int:isbn>', methods=['PATCH'])
def patch_book(isbn):
    data = request.get_json()
    if ("name" in data):
        for book in books:
            if book["isbn"] == isbn:
                book["name"] = data["name"]
                response = Response("",status=204)
                return response

@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    for book in books:
            if book["isbn"] == isbn:
                books.remove(book)
                response = Response("book deleted",status=204)
                return response

app.run(port=5000)