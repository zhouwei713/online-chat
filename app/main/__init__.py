# coding = utf-8
"""
@author: zhou
@time:2019/6/20 10:31
"""

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, forms

