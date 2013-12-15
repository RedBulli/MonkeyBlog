from flask import render_template
from flask.ext.classy import FlaskView

from MonkeyBlog.models.monkey import Monkey


class MonkeysView(FlaskView):
    def get(self):
        monkeys = [Monkey('Sampo', 'sampo@ff.fi'), Monkey('Toinen', 'sampo2@kk.fi')]
        return render_template('monkey_list.html', monkeys=monkeys)
