from flask import request, make_response, jsonify
from flask_restful import Resource
from flask_jwt import jwt_required, current_identity
from ...models import Post, User
from ... import db


class PostsApi(Resource):

    def get(self):
        post_id = request.args.get('post_id')
        user_id = request.args.get('user_id')

        if post_id:
            post = Post.query.get(post_id)

            if post:
                return jsonify(data=post.json())
            else:
                return make_response(
                    jsonify(
                        error={'message': f'No post found with id {post_id}'}
                    ),
                    404
                )

        elif user_id:
            user = User.query.get(user_id)

            if user:
                user_posts = Post.query.filter_by(author_id=user_id) \
                    .order_by(Post.datetime.desc()).all()

                return jsonify(data=[post.json() for post in user_posts])
            else:
                return make_response(
                    jsonify(
                        error={'message': f'No user found with id {user_id}'}
                    ),
                    404
                )

        else:
            posts = Post.query.order_by(Post.datetime.desc()).all()

            return jsonify(data=[post.json() for post in posts])

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

        return make_response(
            jsonify(data=new_post.json(), message='Post created'),
            201
        )

    @jwt_required()
    def put(self):
        req_json = request.get_json()
        post_id = request.args.get('id')
        post = Post.query.get(post_id)

        if post_id is None:
            return make_response(
                jsonify(
                    error={'message': 'Please provide (post_id) parameter'}
                ),
                405
            )
        
        elif post:
            if post.author.id == current_identity.id:
                if req_json.get('title'):
                    post.title = req_json.get('title')
                if req_json.get('description'):
                    post.desc = req_json.get('description')
                if req_json.get('datetime'):
                    post.datetime = req_json.get('datetime')

                db.session.add(post)
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
                jsonify(error={'message': f'No post found with id {post_id}'}),
                404
            )

    @jwt_required()
    def delete(self):
        post_id = request.args.get('id')
        post = Post.query.get(post_id)

        if post:
            if post.author.id == current_identity.id:
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
                    error={'message': f'No post found with id {post_id}'}
                ),
                404
            )
