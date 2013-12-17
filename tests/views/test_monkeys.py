from flask import url_for

from tests import ViewTestCase

from MonkeyBlog.models.monkey import Monkey


class TestMonkeyListing(ViewTestCase):
    render_templates = False

    def test_monkey_list_values(self):
        self.client.get(url_for('MonkeysView:get'))
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
        self.client.post(
            url_for('MonkeysView:post'),
            data={'name': 'Sampo', 'email': 'sampo@kk.fi'}
        )
        assert Monkey.query.count() == prev_monkey_count + 1
        self.assert_template_used('monkey_view.html')
