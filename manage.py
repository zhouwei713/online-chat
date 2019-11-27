# coding = utf-8
"""
@author: zhou
@time:2019/6/20 10:33
"""


import os
from app import create_app, socketio, sch


app = create_app(os.getenv('FLASK_CONFIG') or 'default')


if __name__ == '__main__':
    # app.run(debug=True)
    my = sch.start
    socketio.start_background_task(target=my)
    socketio.run(app, debug=True, host='0.0.0.0', port=8889,)


