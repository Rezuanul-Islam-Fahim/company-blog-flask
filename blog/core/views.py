from flask import Blueprint, render_template, request
from blog.models import Post

core = Blueprint('core', __name__)

@core.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.datetime.desc()).paginate(page=page, per_page=5)

    return render_template('home.html', posts=posts)


@core.route('/info')
def info():
    return render_template('info.html')
