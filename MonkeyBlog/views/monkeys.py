from flask import render_template, request, redirect, url_for
from flask.ext.classy import FlaskView, route

from MonkeyBlog.models.monkey import Monkey
from MonkeyBlog.forms.monkey_form import MonkeyForm
from MonkeyBlog.extensions import db


class MonkeysView(FlaskView):
    def get(self, id):
        monkey = Monkey.query.get(id)
        form = MonkeyForm(obj=monkey)
        return render_template('monkey_view.html', monkey=monkey, form=form)

    def index(self):
        monkeys = Monkey.query.all()
        return render_template('monkey_list.html', monkeys=monkeys)

    def create(self):
        form = MonkeyForm()
        return render_template('monkey_create.html', form=form)

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

    @route('<id>', methods=['POST'])
    def update(self, id):
        monkey = Monkey.query.get(id)
        form = MonkeyForm(request.form, monkey)
        if not form.validate():
            return render_template('monkey_view.html', form=form, monkey=monkey)
        else:
            form.populate_obj(monkey)
            db.session.commit()
            return render_template('monkey_view.html', form=form, monkey=monkey)

    @route('<id>/delete', methods=['POST'])
    def destroy(self, id):
        monkey = Monkey.query.get(id)
        db.session.delete(monkey)
        db.session.commit()
        return redirect(url_for('MonkeysView:index'))
