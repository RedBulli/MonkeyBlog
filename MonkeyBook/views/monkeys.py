from flask import render_template, request, redirect, url_for, abort
from flask.ext.classy import FlaskView, route
from flask.ext.sqlalchemy import Pagination

from sqlalchemy import func
from sqlalchemy.orm import aliased

from MonkeyBook.models.monkey import Monkey, monkey_friends
from MonkeyBook.forms.monkey_form import MonkeyForm
from MonkeyBook.extensions import db


PAGINATION_PAGE_SIZE = 5


class MonkeyListQueries:
    def get_paginated_monkeys(self, order_by, direction, page, page_size):
        if (order_by == 'friends'):
            return self.get_paginated_monkeys_ordered_by_friends_count(
                direction, page, page_size)
        elif (order_by == 'best_friend'):
            query = self.get_monkeys_ordered_by_best_friend_name_query(
                direction)
        else:
            query = self.get_monkeys_ordered_by_name_query(direction)
        return query.paginate(page, page_size)

    def get_paginated_monkeys_ordered_by_friends_count(self, direction, page, 
                                                       page_size):
        query = self.get_monkeys_ordered_by_friends_count_query(direction)
        pagination = self.paginate(query, page, page_size)
        pagination.items = self.get_monkeys_from_list_of_tuples(
            pagination.items)
        return pagination

    def get_monkeys_from_list_of_tuples(self, tuples):
        monkeys = []
        for row in tuples:
            row[0].friend_count = row[1]
            monkeys.append(row[0])
        return monkeys

    def get_monkeys_ordered_by_friends_count_query(self, direction):
        return db.session.query(Monkey, 
                func.count(monkey_friends.c.monkey_id).label('friend_count')
            ).outerjoin(
                monkey_friends, monkey_friends.c.monkey_id == Monkey.id
            ).group_by(Monkey).order_by('friend_count ' + direction)

    def get_monkeys_ordered_by_best_friend_name_query(self, direction):
        best_friend_table = aliased(Monkey)
        query = Monkey.query \
            .outerjoin(
                best_friend_table, 
                best_friend_table.id == Monkey.best_friend_id
            ).order_by('monkey_1.name ' + direction + ' NULLS LAST')
        return query

    def get_monkeys_ordered_by_name_query(self, direction):
        return Monkey.query.order_by('name ' + direction)

    def paginate(self, query, page, per_page=20, error_out=True):
        if error_out and page < 1:
            abort(404)
        items = query.limit(per_page).offset((page - 1) * per_page).all()
        if not items and page != 1 and error_out:
            abort(404)

        if page == 1 and len(items) < per_page:
            total = len(items)
        else:
            total = query.order_by(None).count()

        return Pagination(query, page, per_page, total, items)


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
        if (page == None):
            page = 1
        return int(page)


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
