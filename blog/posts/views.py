from flask import Blueprint, render_template, request, url_for

from blog.models import User, Post

posts = Blueprint('posts', __name__)


@posts.route('/<username>')
def user_posts(username):

    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=user).order_by(
        Post.datetime.desc()).paginate(page=page, per_page=5)

    return render_template('user-blog-posts.html', user=user)
