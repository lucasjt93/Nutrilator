import os

from flask import Flask, render_template, g

from Nutrilator.db import get_db


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

    # Index view TODO user:index display last foods/days if achieved macro intake
    @app.route("/")
    def index():
        if g.user:
            user_data = get_db().execute(
                'SELECT * FROM users_data WHERE user_id = ? ORDER BY date desc LIMIT 1', (g.user['id'],)
            ).fetchone()

            user_macros = get_db().execute(
                'SELECT * FROM macros WHERE user_id = ? ORDER BY date desc LIMIT 1', (g.user['id'],)
            ).fetchone()
            return render_template('index.html', user_data=user_data, user_macros=user_macros)
        else:
            return render_template('index.html')

    # Auth bp
    from . import auth
    app.register_blueprint(auth.bp)

    # Calculator bp TODO check how to mantain one row per user for macros/user_data
    from . import calculator
    app.register_blueprint(calculator.bp)

    # TODO create food database

    return app
