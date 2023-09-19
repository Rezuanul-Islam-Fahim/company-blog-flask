from flask import Flask
from blog.core.views import core
from blog.error.handler import error

app = Flask(__name__)

app.register_blueprint(core)
app.register_blueprint(error)
