from wtforms import Form
from wtforms.fields import StringField, IntegerField
from wtforms.validators import Email, Length, DataRequired


class MonkeyForm(Form):
    name = StringField('name', validators=[Length(min=2, max=64)])
    email = StringField('email', validators=[Email()])
    age = IntegerField('age', validators=[DataRequired()])
