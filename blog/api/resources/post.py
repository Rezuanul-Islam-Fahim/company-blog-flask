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
