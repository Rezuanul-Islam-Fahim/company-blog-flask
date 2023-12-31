from .. import app, login_manager
from .posts.views import posts
from .auth.views import auth
from .core.views import core
from .error.handler import error


def init_web_app():

    app.template_folder = 'web/templates'
    app.static_folder = 'web/static'

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    app.register_blueprint(core)
    app.register_blueprint(error)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(posts, url_prefix='/posts')
