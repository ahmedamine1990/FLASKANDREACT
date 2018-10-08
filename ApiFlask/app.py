from flask import Flask , jsonify , request , Response 
import json
from settings import *
from BookModel import *


@app.route('/')
def hello_to_myapi():
    return 'Hello to My Api Rest with Flask'

@app.route('/books')
def get_books():
    return jsonify(get_all_books())

@app.route('/books/<int:isbn>')
def get_book(isbn):
    return jsonify(get_book_byisbn(isbn))

def check_book(book):
    if ("name" in book and "price" in book and "isbn" in book):
        return "True"
    else : 
        return "False"

@app.route('/books',methods=['POST'])
def Add_book():
    data = request.get_json()
    if (check_book(data)== "True"):
        add_book(data["name"],data["price"],data["isbn"])
        response = Response("Book Added",201,mimetype='application/json')
        response.headers['Location'] = '/books/' + str (data["isbn"])
        return response
    else: 
        errorInvalidObjectMessage = {
            "error" : "invalid book object passed in request",
            "helpString": "object should be similar to {'name': 'bookname', 'price': 'bookprice' , 'isbn' : 'bookisbn'}"
        }
        response = Response(json.dumps(errorInvalidObjectMessage),400,mimetype='application/json')
        return response


@app.route('/books/<int:isbn>', methods=['Delete'])
def Delete_book(isbn):
    operationResult = delete_book(isbn)
    if (operationResult == "True"):
        response = Response(json.dumps("Book Deleted"),206,mimetype='application/json')
        return response
    else :
        errorInvalidObjectMessage = {
            "error" : "book not found"
        }
        response = Response(json.dumps(errorInvalidObjectMessage),400,mimetype='application/json')
        return response


@app.route('/books/<int:isbn>', methods=['PUT'])
def Replacebook(isbn):
    data = request.get_json()
    if (check_book(data)== "True"):
        operationResult=replace_book(data["isbn"],data["name"],data["price"])
        if (operationResult == "True"):
            response = Response(json.dumps("Book Updated"),202,mimetype='application/json')
            return response
        else :
            errorInvalidObjectMessage = {
                "error" : "book not found"
            }
            response = Response(json.dumps(errorInvalidObjectMessage),400,mimetype='application/json')
            return response
    else: 
        errorInvalidObjectMessage = {
            "error" : "invalid book object passed in request",
            "helpString": "object should be similar to {'name': 'bookname', 'price': 'bookprice' , 'isbn' : 'bookisbn'}"
        }
        response = Response(json.dumps(errorInvalidObjectMessage),400,mimetype='application/json')
        return response

@app.route('/books/<int:isbn>', methods=['PATCH'])
def patch_book(isbn):
    data = request.get_json()
    if ("name" in data or "price" in data):
        if ("name" in data):
            operationResult=update_book(isbn,"name",data["name"])
        if ("price" in data):
            operationResult=update_book(isbn,"price",data["price"])
        if (operationResult == "True"):
            response = Response(json.dumps("Book Updated"),202,mimetype='application/json')
            return response
        else :
            errorInvalidObjectMessage = {
                "error" : "book not found"
            }
            response = Response(json.dumps(errorInvalidObjectMessage),400,mimetype='application/json')
            return response  
    else:
        errorInvalidObjectMessage = {
            "error" : "invalid book object passed in request",
            "helpString": "object should be similar to {'name': 'bookname'} or  {'price': 'bookprice'}"
        }
        response = Response(json.dumps(errorInvalidObjectMessage),400,mimetype='application/json')
        return response

app.run(port=5000)