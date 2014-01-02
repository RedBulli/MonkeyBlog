from flask import render_template, request, redirect, url_for
from flask.ext.classy import FlaskView, route

from MonkeyBook.models.monkey import Monkey
from MonkeyBook.forms.monkey_form import MonkeyForm
from MonkeyBook.extensions import db
from MonkeyBook.views.monkey_list_queries import MonkeyListQueries


PAGINATION_PAGE_SIZE = 5


class MonkeyViewHelper:
    def create_monkey(self, form):
        monkey = Monkey()
        form.populate_obj(monkey)
        best_friend = monkey.best_friend
        monkey.best_friend = None
        db.session.add(monkey)
        db.session.commit()
        monkey.best_friend = best_friend
        db.session.commit()
        return monkey

    def update_monkey(self, monkey, form):
        form.populate_obj(monkey)
        best_friend = monkey.best_friend
        monkey.best_friend = None
        db.session.commit()
        monkey.best_friend = best_friend
        db.session.commit()

    def delete_monkey(self, id):
        monkey = Monkey.query.get(id)
        db.session.delete(monkey)
        db.session.commit()

    def get_direction_param(self, request):
        direction = request.args.get('direction')
        if (direction != 'DESC'):
            return 'ASC'
        else:
            return 'DESC'

    def get_order_by_param(self, request):
        order_by = request.args.get('order_by')
        if (order_by != 'friends' and order_by != 'best_friend'):
            order_by = 'name'
        return order_by

    def get_page_param(self, request):
        page = request.args.get('page')
        try:
            page = int(page)
        except (TypeError, ValueError):
            page = 1
        return page


class MonkeysView(FlaskView):
    def index(self):
        order_by = MonkeyViewHelper().get_order_by_param(request)
        direction = MonkeyViewHelper().get_direction_param(request)
        page = MonkeyViewHelper().get_page_param(request)
        pagination = MonkeyListQueries().get_paginated_monkeys(
            order_by, direction, page, PAGINATION_PAGE_SIZE)
        return render_template(
            'monkey_list.html', 
            monkeys=pagination.items, 
            order_by=order_by, 
            direction=direction,
            pagination=pagination,
            page=page
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
