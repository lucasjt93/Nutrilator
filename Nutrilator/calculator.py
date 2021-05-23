from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from Nutrilator.auth import login_required
from Nutrilator.db import get_db

bp = Blueprint('calculator', __name__)


@bp.route('/calculator', methods=('GET', 'POST'))
@login_required
def calculator():
    # get username + message
    username = get_db().execute('SELECT username FROM users WHERE id = ?', (g.user['id'],)).fetchone()
    message = f'Hi {username[0]}, calculate your macros!'

    if request.method == 'POST':
        # get arguments for calculation
        age = request.form['age']
        gender = request.form['gender']
        weight = request.form['weight']
        height = request.form['height']
        activity = request.form['activity']
        goal = request.form['goal']

        # define required fields
        required = {
            'age':age,
            'gender':gender,
            'weight':weight,
            'height':height,
            'activity':activity,
            'goal':goal
        }

        # handles none in required
        for k, v in required.items():
            if not v:
                print(k)
                flash(f'Missing required field {k}', category="error")
                return render_template('calculator/calculator.html', message=message), 403

        #TODO do the calculation and render calculated.html template
    return render_template('calculator/calculator.html', message=message)
