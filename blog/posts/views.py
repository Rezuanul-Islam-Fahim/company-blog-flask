from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import current_user, login_required
from blog import db
from blog.models import User, Post
from blog.posts.forms import BlogPostForm
from blog.models import Post

posts = Blueprint('posts', __name__)


@posts.route('/<username>')
def user_posts(username):

    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=user).order_by(
        Post.datetime.desc()).paginate(page=page, per_page=5)

    return render_template('user-blog-posts.html', user=user, posts=posts)


@posts.route('/blog_posts')
def blog_posts():
    pass


@posts.route('/create')
@login_required
def create_post():

    form = BlogPostForm()

    if form.validate_on_submit():

        new_post = Post(
            title=form.title,
            desc=form.description,
            author_id=current_user.id
        )
        db.session.add(new_post)
        db.session.commit()
        flash('New post created')

        return redirect(url_for('core.home'))

    return render_template('create-post.html')
