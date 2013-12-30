import os

from flask import Flask

from .extensions import db


class Application(Flask):
    def __init__(self, environment=None):
        super(Application, self).__init__(__name__)
        self._init_settings(environment)
        self._init_extensions()
        self._init_blueprints()

    def _init_settings(self, environment=None):
        if environment is None:
            environment = os.environ.get('FLASK_ENV', 'development')
        settings_module = 'MonkeyBook.settings.' + environment
        self.config.from_object(settings_module)

    def _init_extensions(self):
        db.init_app(self)

    def _init_blueprints(self):
        from .views.index import IndexView
        IndexView.register(self)

        from .views.monkeys import MonkeysView
        MonkeysView.register(self)
