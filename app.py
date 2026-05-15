# -*- coding: utf-8 -*-
from functools import wraps
from flask import Flask, render_template, request, session, redirect, url_for, flash
from book import Book

app = Flask(__name__)
app.secret_key = 'quest-secret-2025'


@app.template_filter('phone_fmt')
def phone_fmt(value):
    p = str(value).replace('+', '').replace(' ', '')
    if len(p) == 11:
        return f"+{p[0]} ({p[1:4]}) {p[4:7]}-{p[7:9]}-{p[9:11]}"
    return value

book = Book()


def current_user():
    uid = session.get('user_id')
    return book.GetUser(uid) if uid else None


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            flash('Войдите в аккаунт')
            return redirect(url_for('login'))
        return fn(*args, **kwargs)
    return wrapper


# ─── Public ──────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    if session.get('user_id'):
        return redirect(url_for('quests'))
    return render_template('index.html', user=None)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = book.Login(request.form.get('phone', ''), request.form.get('password', ''))
        if user:
            session['user_id'] = user.id
            return redirect(url_for('index'))
        flash('Неверный номер телефона или пароль')
    return render_template('login.html', user=current_user())


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        errors = book.Register(request.form)
        if not errors:
            flash('Регистрация прошла успешно! Войдите в аккаунт.')
            return redirect(url_for('login'))
        for e in errors:
            flash(e)
    return render_template('register.html', user=current_user())


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        errors = book.ResetPassword(request.form)
        if not errors:
            flash('Пароль успешно изменён')
            return redirect(url_for('login'))
        for e in errors:
            flash(e)
    return render_template('forgot_password.html', user=None)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


# ─── Quests ──────────────────────────────────────────────────────────────────

@app.route('/quests')
def quests():
    return render_template('quests.html', quests=book.GetQuests(), user=current_user())


@app.route('/quest/<int:quest_id>')
@login_required
def quest_detail(quest_id):
    quest = book.GetQuest(quest_id)
    if not quest:
        flash('Квест не найден')
        return redirect(url_for('quests'))
    return render_template('quest_detail.html', quest=quest, user=current_user())


@app.route('/quest/<int:quest_id>/slots')
@login_required
def quest_slots(quest_id):
    quest = book.GetQuest(quest_id)
    if not quest:
        flash('Квест не найден')
        return redirect(url_for('quests'))
    return render_template('quest_slots.html', quest=quest,
                           slots_grouped=book.GetSlotsGrouped(),
                           user=current_user())


@app.route('/quest/<int:quest_id>/confirm')
@login_required
def quest_confirm(quest_id):
    quest = book.GetQuest(quest_id)
    slot = request.args.get('slot', '')
    if not quest or not slot:
        return redirect(url_for('quest_slots', quest_id=quest_id))
    parts = slot.split(' ')
    date = parts[0] if len(parts) > 0 else ''
    time = parts[1] if len(parts) > 1 else ''
    return render_template('quest_confirm.html', quest=quest,
                           slot=slot, date=date, time=time,
                           user=current_user())


# ─── Bookings ────────────────────────────────────────────────────────────────

@app.route('/bookings')
@login_required
def my_bookings():
    user = current_user()
    return render_template('my_bookings.html',
                           bookings=book.GetUserBookings(user.id),
                           qmap=book.QuestsMap(), user=user)


@app.route('/booking/add', methods=['POST'])
@login_required
def add_booking():
    errors = book.AddBooking(session['user_id'], request.form)
    for e in errors:
        flash(e)
    if errors:
        return redirect(url_for('quest_detail', quest_id=request.form.get('quest_id', 0)))
    return redirect(url_for('my_bookings'))



@app.route('/booking/edit/<int:booking_id>', methods=['POST'])
@login_required
def edit_booking(booking_id):
    errors = book.UpdateBooking(session['user_id'], booking_id, request.form)
    for e in errors:
        flash(e)
    if not errors:
        flash('Бронирование обновлено')
    return redirect(url_for('my_bookings'))


@app.route('/booking/delete/<int:booking_id>', methods=['POST'])
@login_required
def delete_booking(booking_id):
    book.DeleteBooking(session['user_id'], booking_id)
    return redirect(url_for('my_bookings'))


# ─── Reviews ─────────────────────────────────────────────────────────────────

@app.route('/reviews')
@login_required
def my_reviews():
    user = current_user()
    return render_template('my_reviews.html',
                           reviews=book.GetUserReviews(user.id),
                           qmap=book.QuestsMap(), user=user)


@app.route('/review/add', methods=['GET', 'POST'])
@login_required
def add_review():
    if request.method == 'POST':
        errors = book.AddReview(session['user_id'], request.form)
        if not errors:
            return redirect(url_for('my_reviews'))
        for e in errors:
            flash(e)
    return render_template('add_review.html', quests=book.GetQuests(), user=current_user())


@app.route('/review/edit/<int:review_id>', methods=['GET', 'POST'])
@login_required
def edit_review(review_id):
    review = book.GetReview(review_id)
    if not review or review.user_id != session['user_id']:
        flash('Отзыв не найден')
        return redirect(url_for('my_reviews'))
    if request.method == 'POST':
        errors = book.UpdateReview(session['user_id'], review_id, request.form)
        if not errors:
            flash('Отзыв обновлён')
            return redirect(url_for('my_reviews'))
        for e in errors:
            flash(e)
    return render_template('edit_review.html', review=review,
                           quest=book.GetQuest(review.quest_id), user=current_user())


@app.route('/review/delete/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    book.DeleteReview(session['user_id'], review_id)
    return redirect(url_for('my_reviews'))


# ─── Profile ─────────────────────────────────────────────────────────────────

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = current_user()
    if request.method == 'POST':
        errors = book.UpdateProfile(user, request.form)
        if not errors:
            flash('Профиль обновлён')
            return redirect(url_for('profile'))
        for e in errors:
            flash(e)
    editing = request.args.get('edit') == '1'
    return render_template('profile.html', user=user, editing=editing)


# ─── Admin ───────────────────────────────────────────────────────────────────

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html', users=book.GetAllUsers(), user=current_user())


@app.route('/admin/user/add', methods=['POST'])
@login_required
def admin_add_user():
    errors = book.Register(request.form)
    if errors:
        for e in errors: flash(e)
    else:
        flash('Пользователь добавлен')
    return redirect(url_for('admin'))


@app.route('/admin/user/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_user(user_id):
    target = book.GetUser(user_id)
    if not target:
        flash('Пользователь не найден')
        return redirect(url_for('admin'))
    if request.method == 'POST':
        errors = book.UpdateProfile(target, request.form)
        if not errors:
            flash('Пользователь обновлён')
            return redirect(url_for('admin'))
        for e in errors: flash(e)
    return render_template('admin_user_form.html', target=target, user=current_user())


@app.route('/admin/user/delete/<int:user_id>', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    if user_id == session.get('user_id'):
        flash('Нельзя удалить себя')
        return redirect(url_for('admin'))
    book.DeleteUser(user_id)
    flash('Пользователь удалён')
    return redirect(url_for('admin'))


@app.teardown_appcontext
def teardown(ctx):
    book.storage.Store()


if __name__ == '__main__':
    app.run(debug=True)
