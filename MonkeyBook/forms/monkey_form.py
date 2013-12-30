from wtforms import Form
from wtforms.fields import StringField, IntegerField
from wtforms.validators import (
    Email, Length, DataRequired, NumberRange, ValidationError
)
from wtforms.ext.sqlalchemy.fields import (
    QuerySelectMultipleField, QuerySelectField
)

from MonkeyBook.models.monkey import Monkey


def validate_best_friend_is_a_friend(form, field):
    if (field.data != None):
        if (field.data not in form.friends.data):
            raise ValidationError('Best friend must be a friend')
    return    

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
    age = IntegerField(
        u'Age', 
        validators=[DataRequired(), NumberRange(min=0, max=200)]
    )
    friends = QuerySelectMultipleField(
        u'Friends',
        get_label='name',
        allow_blank=True
    )
    best_friend = QuerySelectField(
        u'Best Friend',
        get_label='name',
        allow_blank=True,
        validators=[validate_best_friend_is_a_friend]
    )

    
