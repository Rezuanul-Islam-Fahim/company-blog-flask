from flask import request, Response, json, jsonify
from flask_restful import Resource
from sqlalchemy import or_
from ... import db
from ...models import User


class RegisterApi(Resource):

    def post(self):
        req_json = request.get_json()

        if req_json.get('username') is None or \
                req_json.get('email') is None or \
                req_json.get('password') is None:
            return Response(
                response=json.dumps(
                    {'error': {'message': 'Please provide username, email & password '}}
                ),
                status=405,
                mimetype='application/json'
            )

        user = User.query.filter(
            or_(
                User.username == req_json.get('username'),
                User.email == req_json.get('email')
            )
        ).first()

        if user:
            if user.username == req_json.get('username'):
                return Response(
                    response=json.dumps(
                        {'error': {'message': 'Username is already taken'}}
                    ),
                    status=403,
                    mimetype='application/json'
                )
            elif user.email == req_json.get('email'):
                return Response(
                    response=json.dumps(
                        {'error': {'message': 'Email is already taken'}}
                    ),
                    status=403,
                    mimetype='application/json'
                )

        new_user = User(**req_json)
        db.session.add(new_user)
        db.session.commit()

        return jsonify(
            message='Account created successfully',
            user=new_user.json()
        )
