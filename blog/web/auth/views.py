from flask import Blueprint, flash, redirect, url_for, render_template, request
from flask_login import login_user, logout_user, login_required, current_user

from ... import db
from ...models import User
from ..auth.forms import Login, Register, UpdateUser
from ..auth.picture_handler import add_profile_pic

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

        flash('Successfully created a new account')

        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():

    form = Login()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('You have successfully logged in')

            next = request.args.get('next')

            if next is None or not next[0] == '/':
                next = url_for('core.home')

            return redirect(next)

    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')

    return redirect(url_for('core.home'))


@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    form = UpdateUser()

    if form.validate_on_submit():

        if form.profile_img.data:
            username = current_user.username
            pic = add_profile_pic(form.profile_img.data, username)
            current_user.profile_img = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your profile has been updated')

        return redirect(url_for('auth.profile'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_img = url_for(
        'static',
        filename='profile_imgs/' + current_user.profile_img
    )

    return render_template('profile.html', form=form, profile_img=profile_img)
