from flask import render_template, request, redirect, url_for
from flask.ext.classy import FlaskView, route

from sqlalchemy import func
from sqlalchemy.orm import aliased

from MonkeyBook.models.monkey import Monkey, monkey_friends
from MonkeyBook.forms.monkey_form import MonkeyForm
from MonkeyBook.extensions import db


class MonkeyQueries:
    def get_monkeys(self, order_by, direction):
        if (order_by == 'friends'):
            return self.get_monkeys_ordered_by_friends_count(direction)
        elif (order_by == 'best_friend'):
            return self.get_monkeys_ordered_by_best_friend_name(direction)
        else:
            return self.get_monkeys_ordered_by_name(direction)

    def get_monkeys_ordered_by_friends_count(self, direction):
        monkey_tuples = \
            db.session.query(Monkey, 
                func.count(monkey_friends.c.monkey_id).label('friend_count')
            ).outerjoin(
                monkey_friends, monkey_friends.c.monkey_id == Monkey.id
            ).group_by(Monkey).order_by('friend_count ' + direction).all()
        monkeys = []
        for row in monkey_tuples:
            row[0].friend_count = row[1]
            monkeys.append(row[0])
        return monkeys

    def get_monkeys_ordered_by_best_friend_name(self, direction):
        best_friend_table = aliased(Monkey)
        return Monkey.query \
            .outerjoin(
                best_friend_table, 
                best_friend_table.best_friend_id == Monkey.id
            ).order_by('monkey_1.name ' + direction + ' NULLS LAST')

    def get_monkeys_ordered_by_name(self, direction):
        return Monkey.query.order_by('name ' + direction).all()


class MonkeyViewHelper:
    def create_monkey(self, form):
        monkey = Monkey()
        form.populate_obj(monkey)
        db.session.add(monkey)
        db.session.commit()
        return monkey

    def update_monkey(self, monkey, form):
        form.populate_obj(monkey)
        db.session.commit()

    def delete_monkey(self, id):
        monkey = Monkey.query.get(id)
        db.session.delete(monkey)
        db.session.commit()

    def get_direction_param(self, request):
        direction = request.args.get('direction')
        if (direction == None):
            return 'ASC'
        else:
            return 'DESC'

    def get_order_by_param(self, request):
        order_by = request.args.get('order_by')
        if (order_by != 'friends' and order_by != 'best_friend'):
            order_by = 'name'
        return order_by


class MonkeysView(FlaskView):
    def index(self):
        order_by = MonkeyViewHelper().get_order_by_param(request)
        direction = MonkeyViewHelper().get_direction_param(request)
        monkeys = MonkeyQueries().get_monkeys(order_by, direction)
        return render_template(
            'monkey_list.html', 
            monkeys=monkeys, 
            order_by=order_by, 
            direction=direction
        )

    def get(self, id):
        monkey = Monkey.query.get(id)
        form = MonkeyForm(request.form, monkey)
        return render_template('monkey_view.html', monkey=monkey, form=form)

    @route('<id>', methods=['POST'])
    def update(self, id):
        monkey = Monkey.query.get(id)
        form = MonkeyForm(request.form, monkey)
        if form.validate():
            MonkeyViewHelper().update_monkey(monkey, form)
        return render_template('monkey_view.html', form=form, monkey=monkey)

    def create(self):
        form = MonkeyForm(request.form)
        return render_template('monkey_create.html', form=form)

    def post(self):
        form = MonkeyForm(request.form)
        if not form.validate():
            return render_template('monkey_create.html', form=form)
        else:
            monkey = MonkeyViewHelper().create_monkey(form)
            return redirect(url_for('MonkeysView:get', id=monkey.id))

    @route('<id>/delete', methods=['POST'])
    def destroy(self, id):
        MonkeyViewHelper().delete_monkey(id)
        return redirect(url_for('MonkeysView:index'))
