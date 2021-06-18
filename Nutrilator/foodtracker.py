from flask import (
    Blueprint, flash, jsonify, json, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from Nutrilator.auth import login_required
from Nutrilator.db import get_db
from datetime import datetime

bp = Blueprint('foodtracker', __name__)


@bp.route('/foodtracker', methods=('GET', 'POST'))
@login_required
def foodtracker():
    return render_template('foodtracker/foodtracker.html')


@bp.route('/foodtracker/search', methods=('GET', 'POST'))
def search():
    # Look up for food in db
    if request.method == 'POST':
        data = request.get_data().decode()

        # TODO Contact API
        #try:
        #    api_key =


        return jsonify(data)