from flask import request, jsonify
from flask_restful import Resource
from flask_jwt import jwt_required, current_identity
from ...models import Post
from ... import db


class PostApi(Resource):

    def get(self):
        post_id = request.args.get('id')
        post = Post.query.get(post_id)

        if post:
            return jsonify(data=post.json())
        else:
            return jsonify(error={'message': f'No post found with id {post_id}'})

    @jwt_required()
    def post(self):
        req_json = request.get_json()
        new_post = Post(
            title=req_json['title'],
            desc=req_json['description'],
            author_id=current_identity.id
        )
        db.session.add(new_post)
        db.session.commit()

        return jsonify(message='Post created', data=new_post.json())

    @jwt_required()
    def put(self):
        req_json = request.get_json()
        post_id = request.args.get('id')
        post = Post.query.get(post_id)

        if req_json.get('title'):
            post.title = req_json.get('title')
        if req_json.get('description'):
            post.desc = req_json.get('description')
        if req_json.get('datetime'):
            post.datetime = req_json.get('datetime')

        db.session.add(post)
        db.session.commit()

        return jsonify(message='Post updated', data=post.json())
