from flask.ext.test import TestCase

from MonkeyBlog import Application


class BaseTestCase(TestCase):
    teardown_delete_data = True

    @classmethod
    def create_app(cls):
        return Application('test')

    def destroy_app(self):
        """
        Clean up references to the Flask app to prevent memory leaks.
        """
        self.app.extensions['sqlalchemy'].app = None

    def before_method_teardown(self, method):
        self.destroy_app()
