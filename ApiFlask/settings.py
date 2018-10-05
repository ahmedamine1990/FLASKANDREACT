from flask import flask

app = Flask('ApiFlask')
app['SQLALCHEMY_DATABASE_URI'] = "sqlite:C:\Users\aachaari\Documents\GitHub\FLASKANDREACT\ApiFlask\database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False