from flask import Flask , jsonify

app = Flask('ApiFlask')

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
def hello_word():
    return 'Hello World!'

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

app.run(port=5000)