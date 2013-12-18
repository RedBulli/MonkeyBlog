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
        self.assert_template_used('monkey_view.html')

class TestMonkeyListing(ViewTestCase):
    render_templates = False

    def test_monkey_list_values(self):
        MonkeyFactory()
        MonkeyFactory()
        self.client.get(url_for('MonkeysView:index'))
        assert len(self.get_context_variable('monkeys')) == Monkey.query.count()
        self.assert_template_used('monkey_list.html')


class TestMonkeyFormView(ViewTestCase):
    render_templates = False

    def test_monkey_form_url(self):
        self.client.get(url_for('MonkeysView:create'))
        self.assert_template_used('monkey_create.html')


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
            data={'name': 'Sampo', 'email': 'sampo@kk.fi', 'age': 28}
        )
        assert Monkey.query.count() == prev_monkey_count + 1
        monkey = Monkey.query.filter(Monkey.email == 'sampo@kk.fi').first()
        self.assert_redirects(
            response, 
            url_for('MonkeysView:get', id=monkey.id)
        )


class TestMonkeyUpdate(ViewTestCase):
    render_templates = False

    def test_monkey_update(self):
        monkey = MonkeyFactory()
        self.client.post(
            url_for('MonkeysView:update', id=monkey.id),
            data={'name': monkey.name, 'email': monkey.email, 'age': 30}
        )
        assert Monkey.query.get(monkey.id).age == 30
        self.assert_template_used('monkey_view.html')

    def test_monkey_update_failure(self):
        monkey = MonkeyFactory()
        self.client.post(
            url_for('MonkeysView:update', id=monkey.id),
            data={'name': monkey.name, 'email': monkey.email, 'age': -1}
        )
        assert Monkey.query.get(monkey.id).age == 28
        assert len(self.get_context_variable('form').errors) > 0
        self.assert_template_used('monkey_view.html')


class TestMonkeyDelete(ViewTestCase):
    render_templates = False

    def test_monkey_deletion(self):
        monkey = MonkeyFactory()
        prev_monkey_count = Monkey.query.count()
        response = self.client.post(
            url_for('MonkeysView:destroy', id=monkey.id)
        )
        assert Monkey.query.count() == prev_monkey_count - 1
        self.assert_redirects(response, url_for('MonkeysView:index'))
