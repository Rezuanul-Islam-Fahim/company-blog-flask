from flask import request, make_response, jsonify
from flask_restful import Resource
from flask_jwt import jwt_required, current_identity
from ...models import User


class AccountApi(Resource):

    @jwt_required()
    def get(self):
        user_id = request.args.get('user_id')
        user = User.query.get(user_id)

        if user:
            if user.id == current_identity.id:
                return jsonify(user=user.json())
            else:
                return make_response(
                    jsonify(error={'message': 'Permission denied'}),
                    403
                )

        else:
            return make_response(
                jsonify(error={'message': f'No user found with id {user_id}'}),
                404
            )
