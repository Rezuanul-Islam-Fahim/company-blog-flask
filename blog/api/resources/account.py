from flask_restful import Resource


class AccountApi(Resource):

    def get(self):
        print('Account api working')
