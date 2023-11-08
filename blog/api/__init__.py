from flask_restful import Api
from flask_jwt import JWT
from .. import app
from .jwt_secure_handler import authentication, identity
from .resources.register import RegisterApi
from .resources.posts import PostsApi


def init_api():
    api = Api(app, prefix='/api')
    JWT(app, authentication, identity)

    api.add_resource(RegisterApi, '/auth/register')
    api.add_resource(PostsApi, '/posts')
