from flask import request, make_response, jsonify
from flask_restful import Resource
from flask_jwt import jwt_required, current_identity
from ...models import User
from ... import db


class AccountApi(Resource):

    @jwt_required()
    def get(self):
        user_id = request.args.get('user_id')
        user = User.query.get(user_id)

        if user_id is None:
            return make_response(
                jsonify(
                    error={'message': 'Please provide (user_id) parameter'}
                ),
                405
            )

        elif user:
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

    @jwt_required()
    def put(self):

        user_id = request.args.get('user_id')
        req_json = request.get_json()
        user = User.query.get(user_id)

        if user_id is None:
            return make_response(
                jsonify(
                    error={'message': 'Please provide (user_id) parameter'}
                ),
                405
            )

        elif user:
            if user.id == current_identity.id:
                if req_json.get('username') is not None:
                    user.username = req_json.get('username')
                if req_json.get('email') is not None:
                    user.email = req_json.get('email')

                db.session.add(user)
                db.session.commit()

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
