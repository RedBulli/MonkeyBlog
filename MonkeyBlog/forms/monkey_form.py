from wtforms import Form
from wtforms.fields import StringField, IntegerField
from wtforms.validators import Email, Length, DataRequired, NumberRange
from wtforms.ext.sqlalchemy.fields import (
    QuerySelectMultipleField, 
    QuerySelectField
)

from MonkeyBlog.models.monkey import Monkey


class MonkeyForm(Form):
    def __init__(self, formdata=None, monkey=None):
        super(MonkeyForm, self).__init__(formdata, monkey)
        self.set_queries_for_monkey(monkey)

    def set_queries_for_monkey(self, monkey=None):
        id = None
        if (monkey != None):
            id = monkey.id
        self.friends.query = Monkey.query.filter(Monkey.id != id)
        self.best_friend.query = Monkey.query.filter(Monkey.id != id)

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
