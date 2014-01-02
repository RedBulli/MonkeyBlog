from MonkeyBook.extensions import db

from sqlalchemy_utils import EmailType


monkey_friends = db.Table('monkey_friends',
    db.Column('monkey_id', db.Integer, db.ForeignKey('monkey.id'),
              primary_key=True
    ),
    db.Column('friend_id', db.Integer, db.ForeignKey('monkey.id'),
              primary_key=True
    )
)

class Monkey(db.Model):
    id = db.Column(db.Integer, autoincrement='ignore_fk', primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(EmailType(), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)

    friends = db.relationship(
        'Monkey', secondary=monkey_friends, 
        primaryjoin=id==monkey_friends.c.monkey_id,
        secondaryjoin=id==monkey_friends.c.friend_id,
        backref='friended_by',
        foreign_keys=[monkey_friends.c.monkey_id, monkey_friends.c.friend_id]
    )

    best_friend_id = db.Column(
        db.Integer, db.ForeignKey('monkey.id', ondelete='SET NULL')
    )
    best_friend = db.relationship(
        'Monkey', uselist=False, foreign_keys=[best_friend_id],
        remote_side=[id], primaryjoin=best_friend_id==id, post_update=True
    )

    def __init__(self, name=None, email=None, age=None, friends=[], 
                 best_friend=None):
        self.name = name
        self.email = email
        self.age = age
        self.friends = friends
        self.best_friend = best_friend

    def __repr__(self):
        return '<{cls} id={id}, name={name}>'.format(
            id=self.id,
            cls=self.__class__.__name__,
            name=self.name
        )
