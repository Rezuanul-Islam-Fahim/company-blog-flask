import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from blog.core.views import core
from blog.error.handler import error

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='my_secret_key',
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'data.sqlite'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)
Migrate(app, db)

app.register_blueprint(core)
app.register_blueprint(error)
