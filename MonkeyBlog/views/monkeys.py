from flask import render_template, request, redirect, url_for
from flask.ext.classy import FlaskView

from MonkeyBlog.models.monkey import Monkey
from MonkeyBlog.forms.monkey_form import MonkeyForm
from MonkeyBlog.extensions import db


class MonkeysView(FlaskView):
    def get(self, id):
        monkey = Monkey.query.get(id)
        return render_template('monkey_view.html', monkey=monkey)

    def index(self):
        monkeys = Monkey.query.all()
        return render_template('monkey_list.html', monkeys=monkeys)

    def post(self):
        if not request.form:
            form = MonkeyForm()
        else:
            form = MonkeyForm(request.form)
        if not form.validate():
            return render_template('monkey_create.html', form=form)
        else:
            monkey = Monkey()
            form.populate_obj(monkey)
            db.session.add(monkey)
            db.session.commit()
            return redirect(url_for('MonkeysView:get', id=monkey.id))

    def delete(self, id):
        monkey = Monkey.query.get(id)
        db.session.delete(monkey)
        db.session.commit()
        return redirect(url_for('MonkeysView:index'))
