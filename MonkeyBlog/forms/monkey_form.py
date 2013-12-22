from wtforms import Form
from wtforms.fields import StringField, IntegerField
from wtforms.validators import Email, Length, DataRequired, NumberRange
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField

from MonkeyBlog.models.monkey import Monkey


def selectable_friends():
    return Monkey.query.order_by('name')


class MonkeyForm(Form):
    name = StringField(u'Name', validators=[Length(min=2, max=64)])
    email = StringField(u'Email', validators=[Email()])
    age = IntegerField(u'Age', validators=[DataRequired(), NumberRange(min=0, max=200)])
    friends = QuerySelectMultipleField(
        u'Friends',
        get_label='name',
        query_factory=selectable_friends, 
        allow_blank=True)
