from flask import render_template, request, redirect, url_for
from flask.ext.classy import FlaskView, route

from sqlalchemy import func

from MonkeyBlog.models.monkey import Monkey, monkey_friends
from MonkeyBlog.forms.monkey_form import MonkeyForm
from MonkeyBlog.extensions import db


class MonkeysView(FlaskView):
    def _set_form_queries(self, form, monkey=None):
        id = None
        if (monkey != None):
            id = monkey.id
        form.friends.query = Monkey.query.filter(Monkey.id != id)
        form.best_friend.query = Monkey.query.filter(Monkey.id != id)

    def _get_form(self, monkey=None):
        form = MonkeyForm(request.form, monkey)
        self._set_form_queries(form, monkey)
        return form

    def _create_monkey(self, form):
        monkey = Monkey()
        form.populate_obj(monkey)
        db.session.add(monkey)
        db.session.commit()
        return monkey

    def _update_monkey(self, monkey, form):
        form.populate_obj(monkey)
        db.session.commit()

    def _delete_monkey(self, id):
        monkey = Monkey.query.get(id)
        db.session.delete(monkey)
        db.session.commit()

    def get(self, id):
        monkey = Monkey.query.get(id)
        form = self._get_form(monkey)
        return render_template('monkey_view.html', monkey=monkey, form=form)

    def index(self):
        order_by = request.args.get('order_by')
        direction = request.args.get('direction')
        if (direction == None):
            direction = 'ASC'
        if (order_by == 'friends'):
            monkey_tuples = \
                db.session.query(Monkey, 
                    func.count(monkey_friends.c.monkey_id).label('friend_count')
                ).outerjoin(monkey_friends, monkey_friends.c.monkey_id == Monkey.id)\
                .group_by(Monkey).order_by('friend_count ' + direction).all()
            monkeys = []
            for row in monkey_tuples:
                row[0].friend_count = row[1]
                monkeys.append(row[0])
        else:
            if (order_by == None):
                order_by = 'name'
            order_by = 'name'
            monkeys = Monkey.query.order_by(order_by + ' ' + direction).all()

        return render_template('monkey_list.html', monkeys=monkeys)

    def create(self):
        form = self._get_form()
        return render_template('monkey_create.html', form=form)

    def post(self):
        form = self._get_form()
        if not form.validate():
            return render_template('monkey_create.html', form=form)
        else:
            monkey = self._create_monkey(form)
            return redirect(url_for('MonkeysView:get', id=monkey.id))

    @route('<id>', methods=['POST'])
    def update(self, id):
        monkey = Monkey.query.get(id)
        form = self._get_form()
        if form.validate():
            self._update_monkey(monkey, form)
        return render_template('monkey_view.html', form=form, monkey=monkey)

    @route('<id>/delete', methods=['POST'])
    def destroy(self, id):
        self._delete_monkey(id)
        return redirect(url_for('MonkeysView:index'))
