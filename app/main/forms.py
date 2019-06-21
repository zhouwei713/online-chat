# coding = utf-8
"""
@author: zhou
@time:2019/6/20 10:33
"""

from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from flask_wtf import FlaskForm
from ..models import User, Permission


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), ])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class CreateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2',
                                                                            message='Password must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Create User')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class CreatePerForm(FlaskForm):
    permissionname = StringField('Permission name', validators=[DataRequired()])
    submit = SubmitField('Create Permission')


class EditUserForm(FlaskForm):
    permission = SelectMultipleField('Permission', coerce=int)
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.permission.choices = [(per.id, per.permission_name)
                                   for per in Permission.query.order_by(Permission.permission_name).all()]
        self.user = user
