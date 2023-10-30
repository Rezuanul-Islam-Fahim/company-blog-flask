from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
from blog.models import User


class Login(FlaskForm):

    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Register(FlaskForm):

    username = StringField('Username:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password:',
        validators=[
            DataRequired(),
            EqualTo('pass_confirm', message='Passwords must match')
        ]
    )
    pass_confirm = PasswordField(
        'Confirm Password:', validators=[DataRequired()]
    )
    submit = SubmitField('Submit')

    def validate_email(self, email):
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError('Email has been registered already')

    def validate_username(self, username):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError('Username has been taken already')


class UpdateUser(FlaskForm):

    username = StringField('Username:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    profile_img = FileField(
        'Select Picture:',
        validators=[FileAllowed(['jpg', 'png'])]
    )
    submit = SubmitField('Submit')
