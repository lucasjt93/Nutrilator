import os

# General config
DATABASE = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
FLASK_ENV = os.getenv("FLASK_ENV")
