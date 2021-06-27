import os

from flask import current_app as app

app.config(DATABASE=os.getenv("DATABASE_URL"))
