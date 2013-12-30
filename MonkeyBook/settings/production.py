# -*- coding: utf-8 -*-
"""
    summaries.settings.production
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains application settings specific to a production
    environment running on Heroku.
"""

import os

#
# Generic
# -------

# If a secret key is set, cryptographic components can use this to sign cookies
# and other things. Set this to a complex random value when you want to use the
# secure cookie for instance.
try:
    SECRET_KEY = os.environ['SECRET_KEY']
except KeyError:
    raise Exception(
        'Application\'s secret key is not set. Secret key is needed to sign '
        "cookies and other things. You can set the secret key by running "
        '"heroku config:add SECRET_KEY=`python manage.py '
        'generate_secret_key`".'
    )

# The debug flag. Set this to True to enable debugging of the application. In
# debug mode the debugger will kick in when an unhandled exception ocurrs and
# the integrated server will automatically reload the application if changes in
# the code are detected.
DEBUG = True
SERVER_NAME = os.environ.get('SERVER_NAME')


#
# SQLAlchemy
# ----------

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


#
# Sentry
# ------

SENTRY_DSN = os.environ.get('SENTRY_DSN')
