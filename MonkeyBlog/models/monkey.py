from MonkeyBlog.extensions import db

from sqlalchemy_utils import EmailType

monkey_friends = db.Table('monkey_friends',
    db.Column('monkey_id', db.Integer, db.ForeignKey('monkey.id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('monkey.id'), primary_key=True)
)

class Monkey(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(EmailType(), nullable=False, unique=True)

    friends = db.relationship('Monkey', 
        secondary=monkey_friends,
        primaryjoin=id==monkey_friends.c.monkey_id,
        secondaryjoin=id==monkey_friends.c.friend_id
    )

    def __init__(self, name, email):
        self.name = name
        self.email = email
