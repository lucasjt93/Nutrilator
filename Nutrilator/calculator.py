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

        print(required)
        print(timestamp)
        # save data into db TODO SAVE INTO MACROS TABLE
        db.execute(
            'INSERT INTO users_data VALUES (?, ?, ?, ?, ?, ?, ?)',(
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

        return render_template(
            'calculator/results.html',
            TDEE=TDEE,
            REE=REE
        )

    return render_template('calculator/calculator.html', message=message)
