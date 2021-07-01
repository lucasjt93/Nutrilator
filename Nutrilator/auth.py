import functools
import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from Nutrilator.db import get_db
from datetime import date

bp = Blueprint('auth', __name__, url_prefix='/auth')
# Get flask env from env variable
env = os.getenv("FLASK_ENV")

#TODO finish logic to write in postgress db
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        check_user = db.execute(
            'SELECT id FROM users WHERE username = ?', (username,)
        )

        if not username:
            error = 'Must provide username'
        elif not password:
            error = 'Must provide password'
        elif check_user:
            error = f'User {username} is already registered, sorry!'

        if error is None:   # Register the user
            db.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                username, generate_password_hash(password)
            )

            flash('User correctly registered', category='message')
            return redirect(url_for('auth.login'))
        else:
            flash(error, category='error')
            return render_template('auth/register.html'), 400

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        )
        print(user)

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user[0].get('password'), password):
            error = 'Incorrect password'

        if error is None:
            # First clear the session
            session.clear()
            # Remember user logged in
            session['user_id'] = user[0].get('id')
            return redirect(url_for('index'))
        else:
            flash(error, category='error')
            return render_template('auth/login.html'), 400

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    # Retrieve date from datetime api
    today = date.today()

    # TODO finish the migration to new DB here
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()
        g.macros = get_db().execute(
            'SELECT * FROM macros WHERE user_id = ?', (user_id,)
        ).fetchone()
        g.log = get_db().execute(
            ''' SELECT SUM(food_kcal) as kcal, 
                SUM(food_carbs) as carbs, 
                SUM(food_protein) as protein, 
                SUM(food_fat) as fat
                FROM food_logs WHERE user_id = ? AND date = ?''',
            (g.user['id'], today,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
