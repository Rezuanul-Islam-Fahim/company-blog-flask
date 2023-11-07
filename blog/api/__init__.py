from flask_restful import Api
from flask_jwt import JWT
from .. import app
from .resources.register import RegisterApi
from .jwt_secure_handler import authentication, identity

api = Api(app)
JWT(app, authentication, identity)


def init_api():
    api.add_resource(RegisterApi, '/api/auth/register')
