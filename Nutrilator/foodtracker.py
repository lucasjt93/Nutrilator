from flask import (
    Blueprint, flash, jsonify, json, g, redirect, render_template, request, url_for
)

import os
import requests

from Nutrilator.auth import login_required
from Nutrilator.db import get_db
from datetime import date

bp = Blueprint('foodtracker', __name__)


@bp.route('/foodtracker', methods=('GET', 'POST'))
@login_required
def foodtracker():
    if request.method == 'POST':
        db = get_db()

        # Retrieve form data from request
        try:
            food_data = {
                'food_name': str(request.form['name']),
                'food_weight': float(request.form['weight']),
                'food_kcal': float(request.form['kcal']),
                'food_carbs': float(request.form['carbs']),
                'food_protein': float(request.form['protein']),
                'food_fat': float(request.form['fat']),
                'quantity': request.form['quantity']
            }
        # if no data selected
        except:
            flash('Select a food from the database', category='error')
            return render_template('foodtracker/foodtracker.html')

        # If quantity is not submitted
        if not food_data['quantity']:
            food_data['quantity'] = 1

        # Retrieve date from datetime api
        today = date.today()

        # Save into db
        db.execute(
            'INSERT INTO food_logs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (
                g.user['id'],
                today,
                food_data['food_name'],
                food_data['food_weight'],
                food_data['food_kcal'],
                food_data['food_carbs'],
                food_data['food_protein'],
                food_data['food_fat'],
                food_data['quantity']
            )
        )
        db.commit()

        return redirect(url_for('index'))

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
