from flask import request, Response, json, jsonify
from flask_restful import Resource
from sqlalchemy import or_
from ... import db
from ...models import User


class RegisterApi(Resource):

    def post(self):
        req_json = request.get_json()
        user = User.query.filter(
            or_(
                User.username == req_json['username'],
                User.email == req_json['email']
            )
        ).first()

        if user:
            if user.username == req_json['username']:
                return Response(
                    response=json.dumps(
                        {'error': {'message': 'Username is already taken'}}
                    ),
                    status=403,
                    mimetype='application/json'
                )
            elif user.email == req_json['email']:
                return Response(
                    response=json.dumps(
                        {'error': {'message': 'Email is already taken'}}
                    ),
                    status=403,
                    mimetype='application/json'
                )

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
