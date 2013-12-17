from tests import BaseTestCase
from tests.factories import MonkeyFactory

from pytest import raises
from sqlalchemy.exc import IntegrityError

from MonkeyBlog.models.monkey import Monkey
from MonkeyBlog.extensions import db


class TestMonkeyColumnExistences(BaseTestCase):
    def setup_method(self, method):
        super(TestMonkeyColumnExistences, self).setup_method(method)
        monkey = MonkeyFactory()
        self.monkey = Monkey.query.get(monkey.id)

    def test_has_column_id(self):
        assert self.monkey.id

    def test_has_column_name(self):
        assert self.monkey.name

    def test_has_column_email(self):
        assert self.monkey.email


class TestMonkeyFriends(BaseTestCase):
    def setup_method(self, method):
        super(TestMonkeyFriends, self).setup_method(method)
        self.friend = MonkeyFactory(name='Ystava')
        monkey = MonkeyFactory()
        self.monkey = Monkey.query.get(monkey.id)

    def test_add_friend(self):
        assert len(self.monkey.friends) == 0
        self.monkey.friends.append(self.friend)
        db.session.commit()
        assert len(self.monkey.friends) == 1
        assert self.monkey.friends[0].name == 'Ystava'

    def test_add_same_friend_twice(self):
        self.monkey.friends.append(self.friend)
        self.monkey.friends.append(self.friend)
        with raises(IntegrityError):
            db.session.commit()


class TestMonkeyBestFriend(BaseTestCase):
    def setup_method(self, method):
        super(TestMonkeyBestFriend, self).setup_method(method)
        self.friend = MonkeyFactory(name='Paras ystava')
        monkey = MonkeyFactory()
        self.monkey = Monkey.query.get(monkey.id)

    def test_add_best_friend(self):
        assert self.monkey.best_friend == None
        self.monkey.best_friend = self.friend
        db.session.commit()
        assert Monkey.query.get(self.monkey.id).best_friend == self.friend
