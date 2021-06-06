from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from Nutrilator.auth import login_required
from Nutrilator.db import get_db
from datetime import date

bp = Blueprint('calculator', __name__)


@bp.route('/calculator', methods=('GET', 'POST'))
@login_required
def calculator():
    # get username + message
    username = get_db().execute('SELECT username FROM users WHERE id = ?', (g.user['id'],)).fetchone()
    message = f'Hi {username[0]}, calculate your macros!'
    timestamp = str(date.today())

    if request.method == 'POST':
        db = get_db()

        # define required fields
        required = {
            'age': int(request.form['age']),
            'gender': request.form['gender'],
            'weight': int(request.form['weight']),
            'height': int(request.form['height']),
            'activity': request.form['activity'],
            'goal': request.form['goal']
        }

        # handles none in required at serve-side (its also checked at client-side)
        for k, v in required.items():
            if not v:
                print(k)
                flash(f'Missing required field {k}', category="error")
                return render_template('calculator/calculator.html', message=message), 403

        # resting energy expenditure (REE)
        if required['gender'] == 'male':
            # male
            REE = 10 * int(required['weight']) + 6.25 * int(required['height']) - 5 * int(required['age']) + 5
        else:
            # female
            REE = 10 * int(required['weight']) + 6.25 * int(required['height']) - 5 * int(required['age']) - 161

        # total daily energy expenditure (TDEE)
        if required['activity'] == 'Sedentary':
            TDEE = REE * 1.2
        elif required['activity'] == 'Light - 3 times per week':
            TDEE = REE * 1.375
        elif required['activity'] == 'Mid - 5 times per week':
            TDEE = REE * 1.55
        else:
            TDEE = REE * 1.725

        # kcal per goal
        if required['goal'] == 'Lose weight':
            TDEE = TDEE - (TDEE * 0.20)
        elif required['goal'] == 'Gain weight':
            TDEE = TDEE + (TDEE * 0.20)

        # save user data into db
        db.execute(
            'INSERT INTO users_data VALUES (?, ?, ?, ?, ?, ?, ?)', (
                g.user['id'],
                required['age'],
                required['gender'],
                required['weight'],
                required['height'],
                required['goal'],
                timestamp
            )
        )
        db.commit()

        # calculate initial macros per kcal
        protein = 0.825 * (required['weight']/0.453592)
        fat = (TDEE * 0.3) / 9
        carbo = (TDEE - (protein * 4) - (fat * 9)) / 4

        # save macros into db
        user_macros = get_db().execute(
            'SELECT * FROM macros WHERE user_id = ?', (g.user['id'],)
        ).fetchone()

        if not user_macros:
            db.execute(
                'INSERT INTO macros VALUES (?, ?, ?, ?, ?)', (
                    g.user['id'],
                    TDEE,
                    protein,
                    carbo,
                    fat
                )
            )
            db.commit()
        else:
            db.execute(
                'UPDATE macros SET tdee = ?, protein = ?, carbo = ?, fat = ? WHERE user_id = ?', (
                    TDEE,
                    protein,
                    carbo,
                    fat,
                    g.user['id']
                )
            )
            db.commit()

        return redirect(url_for('index'))

    return render_template('calculator/calculator.html', message=message)
