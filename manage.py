# coding = utf-8
"""
@author: zhou
@time:2019/6/20 10:33
"""


import os
from app import create_app, socketio


app = create_app(os.getenv('FLASK_CONFIG') or 'default')


if __name__ == '__main__':
    socketio.run(app, debug=True)


