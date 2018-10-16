from flask import Flask , jsonify , request , Response, render_template
import jwt, datetime
import json
from settings import *
from BookModel import *
from userModel import User
from functools import wraps

@app.route('/')
def hello_to_myapi():
    bok=get_all_books()
    return render_template('index.html', title='Home', result=bok)

@app.route('/login', methods=['POST'])
def get_token():
    request_data = request.get_json()
    username = str(request_data['username'])
    password = str(request_data['password'])
    match = User.matchusernamepassword(username,password)
    if match:
        expirationDate = datetime.datetime.utcnow() + datetime.timedelta(seconds=1000)
        token=jwt.encode({'exp': expirationDate},app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        return Response('', 401, mimetype='application/json')
def token_required(f):
    @wraps(f)
    def wrapper(*arg,**kwargs):
        token= request.args.get('token')
        try:
            jwt.decode(token,app.config['SECRET_KEY'])
            return f(*arg,**kwargs)
        except:
            return jsonify({'error':'Need a valid token to view this page'}),401
    return wrapper

@app.route('/books')
@token_required
def get_books():
    return jsonify(get_all_books())

@app.route('/books/<int:isbn>')
@token_required
def get_book(isbn):
    return jsonify(get_book_byisbn(isbn))

@app.route('/books',methods=['POST'])
@token_required
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
@token_required
def Delete_book(isbn):
    operationResult = delete_book(isbn)
    if (operationResult == "True"):
        response = Response(json.dumps("Book Deleted"),204,mimetype='application/json')
        return response
    else :
        errorInvalidObjectMessage = {
            "error" : "book not found"
        }
        response = Response(json.dumps(errorInvalidObjectMessage),400,mimetype='application/json')
        return response

@app.route('/books/<int:isbn>', methods=['PUT'])
@token_required
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
@token_required
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


def check_book(book):
    if ("name" in book and "price" in book and "isbn" in book):
        return "True"
    else : 
        return "False"

app.run(port=5000)