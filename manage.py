#!/usr/bin/env python
import base64
import os

from flask.ext.script import Manager, Server

from MonkeyBlog import Application, models
from MonkeyBlog.extensions import db


app = Application()

manager = Manager(app)
manager.add_command('runserver', Server(host='localhost'))


@manager.shell
def make_shell_context():
    context = {}
    context['app'] = app
    context['db'] = db
    for model in dir(models):
        if model[0].isupper():
            context[model] = getattr(models, model)
    return context


@manager.command
def syncdb():
    """Synchronize the models with the database."""
    app = Application()
    with app.app_context():
        db.drop_all()
        db.create_all()
    #os.system('alembic upgrade head')


@manager.command
def resetdb():
    """Drops all tables and synchronizes the models with the database."""
    dropdb()
    syncdb()


@manager.command
def dropdb():
    """Drops all tables and constraints from the database."""
    db.drop_all()


@manager.command
def generate_secret_key():
    """Generate a good unique secret key."""
    print base64.b64encode(os.urandom(40))


if __name__ == "__main__":
    manager.run()
