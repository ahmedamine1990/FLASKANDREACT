from flask_sqlalchemy import SQLAlchemy
from settings import app

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ =  'users'
    id = db.Column('user_id', db.Integer, primary_key = True)
    username = db.Column(db.String(100),unique = True,nullable=False)
    password = db.Column(db.String(100),nullable=False)  

    def __repr__(self):
        return str({
            'username': self.username,
            'password': self.password
        })
    def matchusernamepassword(_username,_password):
        user = User.query.filter_by(username=_username).filter_by(password=_password).first()
        if user is None:
            return False
        else:
            return True
    
    def getAllUsers():
        return User.query.all()

    def createUser(_username,_password):
        newUser = User(username=_username,password=_password)
        db.session.add(newUser)
        db.session.commit()


#db.create_all()

