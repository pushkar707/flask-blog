from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,ValidationError
from wtforms.validators import DataRequired,Email,EqualTo
from myProject.models import User
from flask_wtf.file import FileAllowed,FileField

def check_username(form , field):
    if User.query.filter_by(username=field.data).first():
        raise ValidationError('Username is already in use.')

def check_email(form, field):
    if User.query.filter_by(email=field.data).first():
        raise ValidationError('Email already registered.')

class LoginForm(FlaskForm):

    email = StringField('email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Submit')


class RegisterationForm(FlaskForm):

    username = StringField('Username',validators=[DataRequired(),check_username])
    email = StringField('Email',validators=[DataRequired(),Email(),check_email])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm')])
    pass_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField('Register')

class UpdateUserForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    picture = FileField('Profile Image', validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Update')