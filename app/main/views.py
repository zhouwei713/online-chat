# coding = utf-8
"""
@author: zhou
@time:2019/6/20 10:33
"""


from flask import render_template, redirect, url_for, request, current_app
from flask_login import login_required, login_user, logout_user, current_user
from . import main
from .. import db
from .forms import LoginForm, CreateUserForm, CreatePerForm, EditUserForm
from ..models import User, Permission, RelUserPermission
import time
import json
from ..socket_conn import socket_send
import hashlib
from ..redis_conn import redis_conn_pool
import requests
# from ..chatbot.views import get_bot_text


# pool = redis.ConnectionPool(host='redis-12143.c8.us-east-1-3.ec2.cloud.redislabs.com', port=12143,
#                             decode_responses=True, password='pkAWNdYWfbLLfNOfxTJinm9SO16eSJFx')
# r = redis.Redis(connection_pool=pool)
r = redis_conn_pool()


@main.route('/adddb/', methods=['GET', 'POST'])
def addbd():
    db.create_all()
    return "OK"


@main.route('/deldb/', methods=['GET', 'POST'])
def delbd():
    db.drop_all()
    return "OK"


@main.route('/adduser/<user>', methods=['GET', 'POST'])
def adduser1(user):
    user = User(username=user, password='admin')
    db.session.add(user)
    db.session.commit()
    return "OK"


@main.route('/adduser/', methods=['GET', 'POST'])
@login_required
def adduser():
    form = CreateUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('adduser.html', form=form)


@main.route('/listuser/', methods=['GET', 'POST'])
@login_required
def listuser():
    user_list = User.query.all()
    return render_template('listuser.html', user_list=user_list)


@main.route('/addper/', methods=['GET', 'POST'])
@login_required
def addper():
    form = CreatePerForm()
    old_per = Permission.query.filter_by(permission_name=form.permissionname.data).first()
    if form.validate_on_submit() and old_per is None:
        per = Permission(permission_name=form.permissionname.data)
        db.session.add(per)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('addper.html', form=form)


@main.route('/edituser/<int:id>/', methods=['GET', 'POST'])
@login_required
def edituser(id):
    user = User.query.filter_by(id=id).first()
    form = EditUserForm(user=user)
    if form.validate_on_submit():
        for p in form.permission.data:
            rup = RelUserPermission(user_id=id, permission_id=p)
            db.session.add(rup)
            db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('edituser.html', form=form)


@main.route('/login/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@main.route('/login_check', methods=['POST'])
def login_check():
    username = request.form.get('Username', '')
    password = request.form.get('Password', '')
    user = User.query.filter_by(username=username).first()
    if request.method == 'POST':
        if user is not None and user.verify_password(password):
            login_user(user)
            return "success"
        else:
            return "error"
    elif request.method == 'GET':
        return render_template('login.html')


@main.route('/logout/')
@login_required
def logout():
    rname = request.args.get("rname", "")
    r.zrem("chat-" + rname, current_user.username)
    logout_user()
    return redirect(url_for('main.login'))


@main.route('/')
def home():
    return render_template('index.html')


@main.route('/index/')
def index():
    return render_template('index.html')


@main.route('/roomlist/', methods=["GET", 'POST'])
def chat_room_list():
    roomlist_tmp = r.keys(pattern='chat-*')
    roomlist = []
    can_create = False
    create_room = Permission.query.filter_by(permission_name='createroom').first()
    if current_user.is_authenticated:
        rel_user_id = RelUserPermission.query.filter_by(user_id=current_user.id).first()
        rel_permission = RelUserPermission.query.filter_by(user_id=current_user.id).first()
        if rel_permission and rel_user_id and create_room:
            rel_permission_id = rel_permission.permission_id
            create_room_id = create_room.id
            if rel_permission_id == create_room_id:
                can_create = True
    for i in roomlist_tmp:
        i_str = str(i)
        istr_list = i_str.split('-', 1)
        roomlist.append(istr_list[1])
    return render_template('chatroomlist.html', roomlist=roomlist, can_create=can_create)


@main.route('/createroom/', methods=["GET", 'POST'])
@login_required
def create_room():
    rname = request.form.get('chatroomname', '')
    if r.exists("chat-" + rname) is False:
        r.zadd("chat-" + rname, 'hi-user', time.time())
        r.zadd("chat-" + rname, current_user.username, 1)
        return redirect(url_for('main.chat', rname=rname))
    else:
        return redirect(url_for('main.chat_room_list'))


@main.route('/joinroom/', methods=["GET", 'POST'])
def join_chat_room():
    rname = request.args.get('rname', '')
    if rname is None:
        return redirect(url_for('main.chat_room_list'))
    if current_user.is_authenticated:
        r.zadd("chat-" + rname, current_user.username, time.time())
    else:
        pass
    return redirect(url_for('main.chat', rname=rname))


@main.route('/chat/', methods=['GET', 'POST'])
def chat():
    rname = request.args.get('rname', "")
    b_user = r.keys('b_user-*')
    b_user_list = []
    for b in b_user:
        b_user_list.append(r.get(b))
    ulist = r.zrange("chat-" + rname, 0, -1)
    messages = r.zrange("msg-" + rname, 0, -1, withscores=True)
    msg_list = []
    for i in messages:
        msg_list.append([json.loads(i[0]), time.strftime("%Y/%m/%d %p%H:%M:%S", time.localtime(i[1]))])
    if current_user.is_authenticated:
        return render_template('chat.html', rname=rname, user_list=ulist, msg_list=msg_list,
                               b_user_list=b_user_list)
    else:
        email = "youke" + "@hihichat.com"
        hash = hashlib.md5(email.encode('utf-8')).hexdigest()
        gravatar_url = 'http://www.gravatar.com/avatar/' + hash + '?s=40&d=identicon&r=g'
        return render_template('chat.html', rname=rname, g=gravatar_url)


@main.route('/api/sendchat/<info>', methods=['GET', 'POST'])
def send_chat(info):
    if current_user.is_authenticated:
        b_user = r.exists('b_user-%s' % current_user.username)
        if b_user:
            data = json.dumps({'code': 201, 'msg': 'Your are under block now!'})
            return data
        rname = request.form.get("rname", "")
        ulist = r.zrange("chat-" + rname, 0, -1)
        if current_user.username in ulist:
            body = {"username": current_user.username, "msg": info}
            r.zadd("msg-" + rname, json.dumps(body), time.time())
            socket_send(info, current_user.username)
            data = json.dumps({'code': 200, 'msg': info})
            return data
        else:
            data = json.dumps({'code': 403, 'msg': 'You are not in this room'})
            return data
    else:
        # base_url = 'http://luobodazahui.top:8889/api/chat/'
        # chat_text = requests.get(base_url + info).text
        chat_text = get_bot_text(info)
        return chat_text


@main.route('/chat/roomuser/list', methods=['GET', 'POST'])
@login_required
def room_user_list():
    rname = request.args.get('rname', "")
    ulist = r.zrange("chat-" + rname, 0, -1)
    b_user = r.keys('b_user-*')
    b_user_list = []
    for b in b_user:
        b_user_list.append(r.get(b))
    return render_template('roomuser_list.html', ulist=ulist, rname=rname, b_user=b_user_list)


@main.route('/chat/block/roomuser/', methods=['GET', 'POST'])
@login_required
def block_roomuser():
    rname = request.args.get('rname', "")
    new_b_user = request.args.get('b_user', "")
    b_time = request.args.get('b_time', "")
    if b_time is "":
        r.set('b_user-' + new_b_user, new_b_user, ex=None)
    else:
        r.set('b_user-' + new_b_user, new_b_user, ex=b_time)
    return redirect(url_for('main.room_user_list', rname=rname))


@main.route('/chat/kick/roomuser/', methods=['GET', 'POST'])
@login_required
def kick_roomuser():
    rname = request.args.get("rname", "")
    del_user = request.args.get("del_user", "")
    r.zrem("chat-" + rname, del_user)
    return redirect(url_for('main.room_user_list', rname=rname))
