from MonkeyBlog.extensions import db

from sqlalchemy_utils import EmailType


class Monkey(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(EmailType(), nullable=False, unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email
