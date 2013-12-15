from flask import url_for

from tests import BaseTestCase


class TestMonkeyListing(BaseTestCase):
    def test_monkey_list_values(self):
        self.client.get(url_for('MonkeysView:get'))
        assert len(self.get_context_variable('monkeys')) == 2
