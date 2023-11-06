from blog.models import User


def authentication(email, password):
    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        return user


def identity(payload):
    user_id = payload['identity']

    return User.query.get(user_id)
