from flask import (
    Blueprint, flash, jsonify, json, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

import os
import requests

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
    # Look up for food in Nutritionix api
    if request.method == 'POST':
        data = request.get_data().decode()

        # Contact API
        try:
            url = f"https://trackapi.nutritionix.com/v2/natural/nutrients"
            json_data = {"query" : data}
            headers = {
                "x-app-id": os.environ.get("APP_ID"),
                "x-app-key": os.environ.get("API_KEY"),
                "Content-Type": "application/json"
            }
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(json_data)
            )
        except requests.RequestException:
            return jsonify(None)

        # Parse response
        try:
            food = response.json()
            response_data = {
                "name": food.get('foods')[0].get('food_name'),
                "weight": food.get('foods')[0].get('serving_weight_grams'),
                "kcal": food.get('foods')[0].get('nf_calories'),
                "carbs": food.get('foods')[0].get('nf_total_carbohydrate'),
                "protein": food.get('foods')[0].get('nf_protein'),
                "fat": food.get('foods')[0].get('nf_total_fat')
            }
            return jsonify(response_data)
        # Handle not found in Nutritionix api
        except (KeyError, TypeError, ValueError):
            return jsonify(None)
