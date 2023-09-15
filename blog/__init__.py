from flask import Flask
from blog.core.views import core

app = Flask(__name__)

app.register_blueprint(core, url_prefix='/')
