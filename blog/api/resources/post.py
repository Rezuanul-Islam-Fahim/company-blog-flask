from flask import request, jsonify
from flask_restful import Resource
from flask_jwt import jwt_required
from ...models import Post


class PostApi(Resource):

    def get(self):
        post_id = request.args.get('id')
        post = Post.query.get(post_id)

        if post:
            return jsonify(data=post.json())
        else:
            return jsonify(error={'message': f'No post found with id {post_id}'})
