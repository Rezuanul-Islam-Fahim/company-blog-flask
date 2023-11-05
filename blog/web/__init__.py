from flask_login import LoginManager
from .. import app
from .posts.views import posts
from .auth.views import auth
from .core.views import core
from .error.handler import error


def initiate_web_app():
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    app.template_folder = 'web/templates'
    app.static_folder = 'web/static'

    app.register_blueprint(core)
    app.register_blueprint(error)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(posts, url_prefix='/posts')
