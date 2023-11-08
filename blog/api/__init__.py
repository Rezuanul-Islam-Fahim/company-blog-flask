from flask_restful import Api
from flask_jwt import JWT
from .. import app
from .jwt_secure_handler import authentication, identity
from .resources.register import RegisterApi
from .resources.posts import PostsApi

api = Api(app)
JWT(app, authentication, identity)


def init_api():
    api.add_resource(RegisterApi, '/api/auth/register')
    api.add_resource(PostsApi, '/api/posts')
