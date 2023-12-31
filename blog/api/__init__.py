from flask_restful import Api
from flask_jwt import JWT
from .. import app
from .jwt_secure_handler import authentication, identity
from .resources.register import RegisterApi
from .resources.posts import PostsApi, PostCreateApi, AllPosts, UserPosts
from .resources.account import AccountApi, AccountUpdateApi


def init_api():
    api = Api(app, prefix='/api')
    JWT(app, authentication, identity)

    api.add_resource(RegisterApi, '/auth/register')
    api.add_resource(PostsApi, '/posts/<int:id>')
    api.add_resource(PostCreateApi, '/posts/create')
    api.add_resource(AllPosts, '/posts/all')
    api.add_resource(UserPosts, '/posts/user/<int:id>')
    api.add_resource(AccountApi, '/account/<int:id>')
    api.add_resource(AccountUpdateApi, '/account/update')
