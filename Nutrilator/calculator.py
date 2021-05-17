from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from Nutrilator.auth import login_required
from Nutrilator.db import get_db

bp = Blueprint('calculator', __name__)


@bp.route('/')
@login_required
def index():
    username = get_db().execute('SELECT username FROM users WHERE id = ?', (g.user['id'],)).fetchone()
    print(username)
    message = f'Hi {username[0]}'
    return render_template('calculator/index.html', message=message)
