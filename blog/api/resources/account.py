from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_jwt import jwt_required, current_identity
from ...models import User
from ... import db


class AccountApi(Resource):

    def get(self, id):
        user = User.query.get(id)

        if user:
            return jsonify(**user.json())

        else:
            return make_response(
                jsonify(error={'message': f'No user found with id {id}'}),
                404
            )


class AccountUpdateApi(Resource):

    @jwt_required()
    def put(self):
        req_json = request.get_json()
        user = User.query.get(current_identity.id)

        if req_json.get('username') is not None:
            user.username = req_json.get('username')
        if req_json.get('email') is not None:
            user.email = req_json.get('email')

        db.session.commit()

        return make_response(
            jsonify(
                message='Account updated successfully',
                user=user.json()
            ),
            200
        )
