from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class AddBookForm(FlaskForm):
    bookname = StringField('name', validators=[DataRequired()])
    bookprice = FloatField('price', validators=[DataRequired()])
    bookisbn =  IntegerField('isbn', validators=[DataRequired())
    submit = SubmitField('Add Book')