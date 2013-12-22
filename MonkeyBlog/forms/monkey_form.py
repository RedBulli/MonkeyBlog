from wtforms import Form
from wtforms.fields import StringField, IntegerField
from wtforms.validators import Email, Length, DataRequired, NumberRange
from wtforms.ext.sqlalchemy.fields import (
    QuerySelectMultipleField, 
    QuerySelectField
)


class MonkeyForm(Form):
    name = StringField(u'Name', validators=[Length(min=2, max=64)])
    email = StringField(u'Email', validators=[Email()])
    age = IntegerField(u'Age', validators=[DataRequired(), NumberRange(min=0, max=200)])
    friends = QuerySelectMultipleField(
        u'Friends',
        get_label='name',
        allow_blank=True)
    best_friend = QuerySelectField(
        u'Best Friend',
        get_label='name',
        allow_blank=True)
