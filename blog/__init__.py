import os
from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

database_uri = os.environ.get('DATABASE_URL')
if database_uri and database_uri.startswith('postgres://'):
    database_uri = database_uri.replace('postgres://', 'postgresql://')

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=os.environ.get('SECRET_KEY'),
    SQLALCHEMY_DATABASE_URI=database_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    JWT_AUTH_URL_RULE='/api/auth/login',
    JWT_AUTH_USERNAME_KEY='email',
    JWT_EXPIRATION_DELTA=timedelta(seconds=1800)
)

login_manager = LoginManager()
db = SQLAlchemy(app)
Migrate(app, db)

from .web import init_web_app
from .api import init_api

init_web_app()
init_api()
