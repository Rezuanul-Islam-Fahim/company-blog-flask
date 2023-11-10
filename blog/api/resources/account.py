from flask import request, jsonify
from flask_restful import Resource
from flask_jwt import jwt_required, current_identity
from ...models import User
from ... import db


class AccountApi(Resource):

    @jwt_required()
    def get(self):

        user = User.query.get(current_identity.id)
        return jsonify(user=user.json())

    @jwt_required()
    def put(self):
        req_json = request.get_json()
        user = User.query.get(current_identity.id)

        if req_json.get('username') is not None:
            user.username = req_json.get('username')
        if req_json.get('email') is not None:
            user.email = req_json.get('email')

        db.session.add(user)
        db.session.commit()

        return jsonify(user=user.json())
