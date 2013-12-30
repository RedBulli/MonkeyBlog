from MonkeyBook.extensions import db

from sqlalchemy_utils import EmailType
from sqlalchemy.schema import ForeignKeyConstraint


monkey_friends = db.Table('monkey_friends',
    db.Column('monkey_id', db.Integer, db.ForeignKey('monkey.id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('monkey.id'), primary_key=True)
)

class Monkey(db.Model):
    __table_args__ = (
        ForeignKeyConstraint(
            ['id', 'best_friend_id'],
            ['monkey_friends.monkey_id', 'monkey_friends.friend_id'],
            name='fk_best_friend_constraint', use_alter=True,
            onupdate="CASCADE", ondelete="CASCADE"
        ),
    )

    id = db.Column(db.Integer, autoincrement='ignore_fk', primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(EmailType(), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)

    friends = db.relationship('Monkey', 
        secondary=monkey_friends,
        primaryjoin=id==monkey_friends.c.monkey_id,
        secondaryjoin=id==monkey_friends.c.friend_id,
        backref='friended_by',
        foreign_keys=[monkey_friends.c.monkey_id, monkey_friends.c.friend_id]
    )

    best_friend_id = db.Column(db.Integer, db.ForeignKey('monkey.id'))
    best_friend = db.relationship(
        'Monkey',
        uselist=False,
        foreign_keys=best_friend_id,
        remote_side=[id],
        primaryjoin=best_friend_id==id,
        post_update=True
    )

    def __init__(self, name=None, email=None, age=None):
        self.name = name
        self.email = email
        self.age = age

    def __repr__(self):
        return '<{cls} id={id}, name={name}>'.format(
            id=self.id,
            cls=self.__class__.__name__,
            name=self.name
        )
