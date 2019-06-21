# coding = utf-8
"""
@author: zhou
@time:2019/6/20 11:50
"""


from . import socketio
from flask_socketio import emit


@socketio.on('request_for_response', namespace='/testnamespace')
def socket_send(data, user):
    emit("response", {"code": '200', "msg": data, "username": user}, broadcast=True, namespace='/testnamespace')


# socketio.on_event('request_for_response', socket_send, namespace='/testnamespace')
