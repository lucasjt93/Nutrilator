import sqlite3
import os
import cs50
import click
from datetime import datetime, timedelta
from flask import current_app, g
from flask.cli import with_appcontext


# Get flask env from env variable
env = os.getenv("FLASK_ENV")
db_name = os.getenv("DATABASE_URL")


def get_db():
    if 'db' not in g:
        # Connect to heroku psql
        if env == "production":

            # Heroku solution for postgres change of domain
            uri = os.getenv("DATABASE_URL")
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
    # Get db from g
    db = g.pop('db', None)

    # Env determination for closing
    if db is not None:
        if env == "development":
            db.close()
        elif env == "production":
            # Workaround for fixing connection limit in postgres with Heroku free account
            utc_time = datetime.utcnow() - timedelta(0, 10)
            db.execute(
                'SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = ? AND state = ? AND state_change < ?',
                db_name[-14:],
                'idle',
                utc_time
            )


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
