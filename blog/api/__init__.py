from flask_restful import Api
from .. import app
from .resources.register import RegisterApi

api = Api(app)


def initiate_api():
    api.add_resource(RegisterApi, '/api/register')
