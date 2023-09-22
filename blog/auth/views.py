from flask import Blueprint, flash, redirect, url_for, render_template, request
from flask_login import login_user, logout_user, login_required
from forms import Login, Register, UpdateUser
from blog.models import User
from blog import db

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST', 'GET'])
def register():

    form = Register()

    if form.validate_on_submit():

        new_user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful')

        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():

    form = Login()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful')

            next = request.args.get('next')

            if next is None or not next[0] == '/':
                next = url_for('core.home')

            return redirect(next)

        return render_template('login.html', form=form)
