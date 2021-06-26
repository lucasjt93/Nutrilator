import os

from flask import Flask, render_template, g

from Nutrilator.db import get_db
from Nutrilator.auth import login_required


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'nutrilator.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initiate db CLI
    from . import db
    db.init_app(app)

    # Index view
    @app.route("/")
    def index():
        if g.user:

            user_data = get_db().execute(
                'SELECT * FROM users_data WHERE user_id = ? ORDER BY date desc LIMIT 1', (g.user['id'],)
            ).fetchone()

            weight_data = get_db().execute(
                'SELECT weight, date FROM users_data WHERE user_id = ?', (g.user['id'],)
            ).fetchall()

            weight_data = [dict(row) for row in weight_data]
            labels = [weight_data[n]['date'][:10] for n in range(len(weight_data))]
            data = [weight_data[n]['weight'] for n in range(len(weight_data))]

            return render_template(
                'index.html',
                user_data=user_data,
                labels=labels,
                data=data
            )
        else:
            return render_template('index.html')

    # Auth bp
    from . import auth
    app.register_blueprint(auth.bp)

    # Calculator bp
    from . import calculator
    app.register_blueprint(calculator.bp)

    # Food tracker bp
    from . import foodtracker
    app.register_blueprint(foodtracker.bp)

    # Food log
    @app.route("/foodlog")
    @login_required
    def foodlog():
        user_log = get_db().execute(
            'SELECT * FROM food_logs WHERE user_id = ? ORDER BY date DESC', (g.user['id'],)
        ).fetchall()
        return render_template('foodlog/foodlog.html', user_log=user_log)

    return app


