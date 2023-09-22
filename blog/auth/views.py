from flask import Blueprint, flash, redirect, url_for, render_template
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

    return render_template('register.html')
