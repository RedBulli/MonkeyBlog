from flask import url_for

from tests import ViewTestCase
from tests.factories import MonkeyFactory

from MonkeyBlog.models.monkey import Monkey


class TestMonkeyView(ViewTestCase):
    render_templates = False

    def test_monkey_view(self):
        monkey = MonkeyFactory()
        self.client.get(url_for('MonkeysView:get', id=monkey.id))
        assert self.get_context_variable('monkey').name == 'Sampo'

class TestMonkeyListing(ViewTestCase):
    render_templates = False

    def test_monkey_list_values(self):
        self.client.get(url_for('MonkeysView:index'))
        assert len(self.get_context_variable('monkeys')) == 2


class TestMonkeyPost(ViewTestCase):
    render_templates = False

    def test_empty_monkey_creation(self):
        self.client.post(
            url_for('MonkeysView:post'),
            data=None
        )
        assert len(self.get_context_variable('form').errors) > 0
        self.assert_template_used('monkey_create.html')

    def test_monkey_creation(self):
        prev_monkey_count = Monkey.query.count()
        response = self.client.post(
            url_for('MonkeysView:post'),
            data={'name': 'Sampo', 'email': 'sampo@kk.fi'}
        )
        assert Monkey.query.count() == prev_monkey_count + 1
        monkey = Monkey.query.filter(Monkey.email == 'sampo@kk.fi').first()
        self.assert_redirects(response, url_for('MonkeysView:get', id=monkey.id))
