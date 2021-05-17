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
    username = get_db().execute('SELECT username FROM users WHERE id = ?', g.user).fetchone()
    message = f'Hi {username}'
    return render_template('Nutrilator/index.html', message=message)
