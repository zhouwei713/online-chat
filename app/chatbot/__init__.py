# coding = utf-8
"""
@author: zhou
@time:2019/6/25 20:08
"""

from flask import Blueprint

chatbot = Blueprint('chatbot', __name__)

from . import views
