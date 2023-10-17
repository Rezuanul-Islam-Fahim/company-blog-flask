from flask import Blueprint, render_template, request, url_for, redirect, flash, abort
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


@posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):

    post = Post.query.get_or_404(blog_post_id)

    return render_template('post.html', post=post)


@posts.route('/create', methods=['POST', 'GET'])
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

    return render_template('create-post.html', form=form)


@posts.route('/<int:blog_post_id>/update', methods=['POST', 'GET'])
@login_required
def update_post(blog_post_id):

    post = Post.query.get_or_404(blog_post_id)

    if post.author != current_user:
        abort(403)

    form = BlogPostForm()

    if form.validate_on_submit():

        post.title = form.title
        post.description = form.description
        db.session.commit()
        flash('Post updated')

        return redirect(url_for('posts.blog_post', blog_post_id=post.id))

    elif request.method == 'GET':
        form.title = post.title
        form.description = post.description

    return render_template('update-post.html', form=form)


@posts.route('/<int:blog_post_id>/delete')
@login_required
def delete_post(blog_post_id):

    post = Post.query.get_or_404(blog_post_id)

    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Blog post deleted')

    return redirect(url_for('core.home'))
