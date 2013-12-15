from tests import BaseTestCase
from tests.factories import MonkeyFactory

from MonkeyBlog.models.monkey import Monkey


class TestMonkeyColumnExistences(BaseTestCase):
    def setup_method(self, method):
        super(TestMonkeyColumnExistences, self).setup_method(method)
        monkey = MonkeyFactory()
        self.monkey = Monkey.query.get(monkey.id)

    def test_has_column_name(self):
        assert self.monkey.name
