from MonkeyBook import Application
from MonkeyBook.extensions import db


def pytest_configure(config):
    app = Application('test')
    with app.app_context():
        db.create_all()


def pytest_unconfigure(config):
    app = Application('test')
    with app.app_context():
        db.drop_all()
