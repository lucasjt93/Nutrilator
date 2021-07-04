import sqlite3
import os
import cs50
import click
from flask import current_app, g
from flask.cli import with_appcontext


# Get flask env from env variable
env = os.getenv("FLASK_ENV")


def get_db():
    if 'db' not in g:
        # Connect to heroku psql
        if env == "production":
            uri = os.getenv("DATABASE_URL")  # or other relevant config var
            if uri.startswith("postgres://"):
                uri = uri.replace("postgres://", "postgresql://", 1)
            # rest of connection code using the connection string `uri`
            g.db = cs50.SQL(uri)
        else:
            # Connect to local sqlite3
            g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    print(f"{db} CLOSING")

    if db is not None:
        if env == "development":
            print("BAD")
            db.close()
        elif env == "production":
            print("GOOD")
            db._disconnect()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    # Clear existing data and create new tables
    init_db()
    click.echo('Db initialized!')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
