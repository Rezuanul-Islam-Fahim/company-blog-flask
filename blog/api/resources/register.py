from flask import request, jsonify
from flask_restful import Resource
from ... import db
from ...models import User


class RegisterApi(Resource):

    def post(self):
        req_json = request.get_json()
        user_by_name = User.query.filter_by(
            username=req_json['username']
        ).first()
        user_by_email = User.query.filter_by(email=req_json['email']).first()

        if user_by_name is not None:
            return jsonify(error={'message': 'Username is already taken'})
        elif user_by_email is not None:
            return jsonify(error={'message': 'Email is already taken'})

        new_user = User(
            username=req_json['username'],
            email=req_json['email'],
            password=req_json['password']
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify(
            message='Account created successfully',
            user=new_user.json()
        )
