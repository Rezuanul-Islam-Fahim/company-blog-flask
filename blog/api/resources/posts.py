from flask import request, make_response, jsonify
from flask_restful import Resource
from flask_jwt import jwt_required, current_identity
from ...models import Post, User
from ... import db


class PostsApi(Resource):

    def get(self, id):

        post = Post.query.get(id)

        if post:
            return jsonify(data=post.json())
        else:
            return make_response(
                jsonify(
                    error={'message': f'No post found with id {id}'}
                ),
                404
            )

    @jwt_required()
    def put(self, id):
        req_json = request.get_json()
        post = Post.query.get(id)

        if post:
            if post.author == current_identity:
                if req_json.get('title'):
                    post.title = req_json.get('title')
                if req_json.get('description'):
                    post.desc = req_json.get('description')
                if req_json.get('datetime'):
                    post.datetime = req_json.get('datetime')

                db.session.commit()

                return jsonify(message='Post updated', data=post.json())

            else:
                return make_response(
                    jsonify(
                        error={'message': 'Post author verfication failed'}
                    ),
                    403
                )

        else:
            return make_response(
                jsonify(error={'message': f'No post found with id {id}'}),
                404
            )

    @jwt_required()
    def delete(self, id):
        post = Post.query.get(id)

        if post:
            if post.author== current_identity:
                db.session.delete(post)
                db.session.commit()

                return jsonify(message='Post deleted')

            else:
                return make_response(
                    jsonify(
                        error={'message': 'Post author verfication failed'}
                    ),
                    403
                )

        else:
            return make_response(
                jsonify(
                    error={'message': f'No post found with id {id}'}
                ),
                404
            )


class PostCreateApi(Resource):

    @jwt_required()
    def post(self):
        req_json = request.get_json()

        if req_json.get('title') is None or req_json.get('description') is None:
            return make_response(
                jsonify(
                    error={'message': 'Please provide (title) & (description)'}
                ),
                405
            )

        else:
            new_post = Post(**req_json, author_id = current_identity.id)

            db.session.add(new_post)
            db.session.commit()

            return make_response(
                jsonify(data=new_post.json(), message='Post created'),
                201
            )


class AllPosts(Resource):

    def get(self):

        posts = Post.query.order_by(Post.datetime.desc()).all()

        return jsonify(data=[post.json() for post in posts])


class UserPosts(Resource):

    def get(self, id):

        user = User.query.get(id)

        if user:
            posts = Post.query.filter_by(author=user) \
                .order_by(Post.datetime.desc()).all()

            return jsonify(data=[post.json() for post in posts])

        else:
            return make_response(
                jsonify(error={'message': f'No user found with id: {id}'}),
                404
            )
