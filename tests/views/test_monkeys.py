from flask import url_for

from tests import ViewTestCase
from tests.factories import MonkeyFactory

from MonkeyBook.models.monkey import Monkey
from MonkeyBook.extensions import db


class TestMonkeyView(ViewTestCase):
    render_templates = False

    def test_monkey_view(self):
        monkey = MonkeyFactory()
        self.client.get(url_for('MonkeysView:get', id=monkey.id))
        assert self.get_context_variable('monkey').name == 'Sampo'
        self.assert_template_used('monkey_view.html')


class TestMonkeyListings(ViewTestCase):
    render_templates = False

    def setup_method(self, method):
        super(TestMonkeyListings, self).setup_method(method)
        MonkeyFactory(name='Sampo')
        MonkeyFactory(name='Aapo')
        MonkeyFactory(name='Heikki')

    def test_monkey_list_values(self):
        self.client.get(url_for('MonkeysView:index'))
        assert len(self.get_context_variable('monkeys')) == Monkey.query.count()
        self.assert_template_used('monkey_list.html')

    def test_monkey_default_ordering_by_name_asc(self):
        self.client.get(url_for('MonkeysView:index'))
        assert self.get_context_variable('monkeys')[0].name == 'Aapo'
        assert self.get_context_variable('monkeys')[1].name == 'Heikki'
        assert self.get_context_variable('monkeys')[2].name == 'Sampo'

    def test_monkey_ordering_by_name_desc(self):
        self.client.get(
            url_for('MonkeysView:index', order_by='name', direction='desc'))
        assert self.get_context_variable('monkeys')[0].name == 'Sampo'
        assert self.get_context_variable('monkeys')[1].name == 'Heikki'
        assert self.get_context_variable('monkeys')[2].name == 'Aapo'


class TestMonkeyListingsOrderingByFriendsCount(ViewTestCase):
    render_templates = False

    def setup_method(self, method):
        super(TestMonkeyListingsOrderingByFriendsCount, self).setup_method(method)
        self.zero_friends = MonkeyFactory(name='Sampo')
        self.two_friends = MonkeyFactory(name='Aapo')
        self.one_friend = MonkeyFactory(name='Heikki')
        self.one_friend.friends.append(self.two_friends)
        self.two_friends.friends.append(self.one_friend)
        self.two_friends.friends.append(self.zero_friends)
        db.session.commit()

    def test_monkey_ordering_by_friend_count_desc(self):
        self.client.get(
            url_for('MonkeysView:index', order_by='friends', direction='desc'))
        assert self.get_context_variable('monkeys')[0] == self.two_friends
        assert self.get_context_variable('monkeys')[1] == self.one_friend
        assert self.get_context_variable('monkeys')[2] == self.zero_friends

    def test_monkey_ordering_by_friend_count_asc(self):
        self.client.get(url_for('MonkeysView:index', order_by='friends'))
        assert self.get_context_variable('monkeys')[0] == self.zero_friends
        assert self.get_context_variable('monkeys')[1] == self.one_friend
        assert self.get_context_variable('monkeys')[2] == self.two_friends


class TestMonkeyListingsOrderingByBestFriendName(ViewTestCase):
    render_templates = False

    def _make_friend_and_best_friend(self, monkey, friend):
        monkey.friends.append(friend)
        db.session.commit()
        monkey.best_friend = friend
        db.session.commit()

    def setup_method(self, method):
        super(TestMonkeyListingsOrderingByBestFriendName, self).setup_method(
            method)
        self.no_best_friend = MonkeyFactory()
        self.sampo_jussi = MonkeyFactory(name='Sampo')
        self.aapo_heikki = MonkeyFactory(name='Aapo')
        self.heikki_aapo = MonkeyFactory(name='Heikki')
        self.jussi_sampo = MonkeyFactory(name='Jussi')
        self._make_friend_and_best_friend(self.sampo_jussi, self.jussi_sampo)
        self._make_friend_and_best_friend(self.jussi_sampo, self.sampo_jussi)
        self._make_friend_and_best_friend(self.heikki_aapo, self.aapo_heikki)
        self._make_friend_and_best_friend(self.aapo_heikki, self.heikki_aapo)

    def test_monkey_ordering_by_friend_count_desc(self):
        self.client.get(
            url_for(
                'MonkeysView:index', order_by='best_friend', direction='desc'))
        assert self.get_context_variable('monkeys')[0] == self.jussi_sampo
        assert self.get_context_variable('monkeys')[1] == self.sampo_jussi
        assert self.get_context_variable('monkeys')[2] == self.aapo_heikki
        assert self.get_context_variable('monkeys')[3] == self.heikki_aapo
        assert self.get_context_variable('monkeys')[4] == self.no_best_friend

    def test_monkey_ordering_by_friend_count_asc(self):
        self.client.get(url_for('MonkeysView:index', order_by='best_friend'))
        assert self.get_context_variable('monkeys')[0] == self.heikki_aapo
        assert self.get_context_variable('monkeys')[1] == self.aapo_heikki
        assert self.get_context_variable('monkeys')[2] == self.sampo_jussi
        assert self.get_context_variable('monkeys')[3] == self.jussi_sampo
        assert self.get_context_variable('monkeys')[4] == self.no_best_friend


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
        friend = MonkeyFactory()
        prev_monkey_count = Monkey.query.count()
        response = self.client.post(
            url_for('MonkeysView:post'),
            data={
                'name': 'Sampo', 
                'email': 'sampo@kk.fi', 
                'age': 28, 
                'friends': friend.id,
                'best_friend': friend.id
            }
        )
        assert Monkey.query.count() == prev_monkey_count + 1
        monkey = Monkey.query.filter(Monkey.email == 'sampo@kk.fi').first()
        self.assert_redirects(
            response, 
            url_for('MonkeysView:get', id=monkey.id)
        )

    def test_monkey_best_friend_validation(self):
        friend = MonkeyFactory()
        prev_monkey_count = Monkey.query.count()
        self.client.post(
            url_for('MonkeysView:post'),
            data={
                'name': 'Sampo', 
                'email': 'sampo@kk.fi', 
                'age': 28, 
                'best_friend': friend.id
            }
        )
        assert Monkey.query.count() == prev_monkey_count
        assert len(self.get_context_variable('form').errors) > 0
        self.assert_template_used('monkey_create.html')


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
        friend = MonkeyFactory()
        monkey = MonkeyFactory()
        friend.friends.append(monkey)
        db.session.commit()
        prev_monkey_count = Monkey.query.count()
        response = self.client.post(
            url_for('MonkeysView:destroy', id=monkey.id)
        )
        assert Monkey.query.count() == prev_monkey_count - 1
        self.assert_redirects(response, url_for('MonkeysView:index'))
