from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from blog import db
from blog import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    profile_img = db.Column(
        db.String(64),
        nullable=False,
        default='default_profile.jpg'
    )
    password_hash = db.Column(db.String(128))
    posts = db.Relationship('Post', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return 'Username: {self.username}, Email: {self.email}'
