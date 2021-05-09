import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from Nutrilator.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        # Ensure username was submitted
        if not username:
            error = 'Must provide username'
            flash(error)
            return redirect(url_for('auth.login'), code=403)
        # Ensure pass was submitted
        elif not password:
            error = 'Must provide password'
            flash(error)
            return redirect(url_for('auth.login'), code=403)
        # Ensure user is unique
        elif db.execute(
            'SELECT id FROM users WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f'User {username} is already registered, sorry!'
            flash(error)
            return redirect(url_for('auth.login'), code=403)

        if error is not None:
            # Save user and pass to db
            db.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html')
