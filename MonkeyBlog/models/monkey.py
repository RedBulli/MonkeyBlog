from MonkeyBlog.extensions import db

from sqlalchemy_utils import EmailType

monkey_friends = db.Table('monkey_friends',
    db.Column('monkey_id', db.Integer, db.ForeignKey('monkey.id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('monkey.id'), primary_key=True)
)

class Monkey(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(EmailType(), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)

    friends = db.relationship('Monkey', 
        secondary=monkey_friends,
        primaryjoin=id==monkey_friends.c.monkey_id,
        secondaryjoin=id==monkey_friends.c.friend_id,
        backref='friended_by'
    )

    best_friend_id = db.Column(db.Integer, db.ForeignKey('monkey.id'))
    best_friend = db.relationship('Monkey', uselist=False)

    def __init__(self, name=None, email=None, age=None):
        self.name = name
        self.email = email
        self.age = age
