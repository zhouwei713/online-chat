# coding = utf-8
"""
@author: zhou
@time:2019/6/20 10:33
"""


from . import db
from . import login_manager
from flask_login import UserMixin
from flask import request
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    avatar_hash = db.Column(db.String(32))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def gravatar(self, name=None, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        if name is not None:
            email = name + "@hihichat.com"
        else:
            email = self.username + "@hihichat.com"
        myhash = self.avatar_hash or hashlib.md5(email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, hash=myhash, size=size,
                                                                     default=default, rating=rating)


class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    permission_name = db.Column(db.String(64), unique=True, index=True)


class RelUserPermission(db.Model):
    __tablename__ = 'reluserpermission'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    permission_id = db.Column(db.Integer)


