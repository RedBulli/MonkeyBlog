from MonkeyBook.extensions import db

from sqlalchemy_utils import EmailType
from sqlalchemy import ForeignKeyConstraint


monkey_friends = db.Table('monkey_friends',
    db.Column(
        'monkey_id', db.Integer,
        db.ForeignKey('monkey.id', onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True
    ),
    db.Column(
        'friend_id', db.Integer,
        db.ForeignKey('monkey.id', onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True
    )
)

best_friends = db.Table('best_friends',
    db.Column('monkey_id', db.Integer, primary_key=True),
    db.Column('friend_id', db.Integer),
    ForeignKeyConstraint(
        ['monkey_id', 'friend_id'],
        ['monkey_friends.monkey_id', 'monkey_friends.friend_id'],
        name='fk_favorite_entry', use_alter=True, onupdate='CASCADE', 
        ondelete='CASCADE'
    )
)


class Monkey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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

    best_friend = db.relationship(
        'Monkey', secondary=best_friends, 
        primaryjoin=id==best_friends.c.monkey_id,
        secondaryjoin=id==best_friends.c.friend_id,
        foreign_keys=[best_friends.c.monkey_id, best_friends.c.friend_id], 
        remote_side=[id], 
        uselist=False, post_update=True, backref='best_friended_by'
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
