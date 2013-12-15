from flask import redirect
from flask.ext.classy import FlaskView


class IndexView(FlaskView):
    route_base= '/'

    def index(self):
        return redirect('/monkeys/')
