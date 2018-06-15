from flask import Flask, jsonify,session,flash
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from room.Room import Room
from room.AI import AI_Room

import ai
import json
import random
import time

app = Flask(__name__)
dict_room = {}
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://qt123:qq1334713380@localhost:3306/gobang"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = "dhiuqheiuqwheqasd"
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(128),unique=True)
    password = db.Column(db.String(128),unique=True)
    sources = db.Column(db.Integer,unique=True)
    


@app.route('/rooms')
def rooms():
    global dict_room
    list_req = []
    for key, room in dict_room.items():
        dict_req = {}
        dict_req["id"] = key
        dict_req['player'] = "%d / 2" % sum(room.list_player)
        dict_req['room'] = "双人" if type(room).__name__ == "Room" else "AI"
        dict_req["name"] = room.name
        list_req.append(dict_req)
    
    return jsonify(list_req)


@app.route('/addRoom')
def add_room():
    # 新建一个普通房间
    global dict_room
    room_name = request.args.get("name")
    room_type = int(request.args.get("type"))
    t = time.time()
    key = str(int(round(t * 1000)))
    if room_type == 1:
        dict_room[key] = Room(key, name=room_name)
    elif room_type == 2:
        dict_room[key] = AI_Room(key, name=room_name)
    return jsonify({"key": key})


@app.route("/openRoom/<string:room_id>")
def open_room(room_id):
    room = None
    if dict_room.get(room_id):
        room = dict_room[room_id]
        if room.isFull():
            return "这个房间已经满了"
    else:
        return
    if type(room).__name__ == "Room":
        return render_template('gobang.html', key=room_id)
    return render_template('gobangAI.html', key=room_id)


@app.route('/AI')
def AI():
    return render_template('gobangAI.html')


@app.route("/dromp/<string:room_id>")
def dromp(room_id):
    room = dict_room[room_id]
    line = int(request.args.get("line"))
    rows = int(request.args.get("row"))
    color = int(request.args.get("color"))
    winner = room.isWinner(line, rows, color)
    if winner < 65534:
        room.now_step += 1
    room.steps.append([line, rows, color])
    dict_req = {"winner": winner, "line": line, "rows": rows, "color": color, "step": room.now_step}
    return json.dumps(dict_req)


@app.route("/drompAI/<string:room_id>")
def drompAI(room_id):
    room = dict_room[room_id]
    room.isAI = True
    line = int(request.args.get("line"))
    rows = int(request.args.get("row"))
    color = int(request.args.get("color"))
    
    winner = room.isWinner(line, rows, color)
    if winner >= 65534:
        winner = 0
    # steps.append([line, rows, color])
    dict_req = {"winner": winner, "line": [line], "rows": [rows]}
    ai_list = room.getBestMove( color * -1)
    #ai_list = ai.getBestMove(room.ponsition, color * -1)
    dict_req["line"].append(ai_list[0])
    dict_req["rows"].append(ai_list[1])
    if winner == 0:
        winner = room.isWinner(ai_list[0], ai_list[1], color * -1)
        dict_req["winner"] = winner
    return json.dumps(dict_req)


@app.route("/player/<string:room_id>")
def player(room_id):
    global dict_room
    room = dict_room[room_id]
    num = int(request.args.get("player"))
    if room.list_player[num]:
        return "NO"
    room.list_player[num] = 1
    if type(room).__name__ == "AI_Room":
        room.list_player[num] = [1,1]
    return "YES"


@app.route("/step/<string:room_id>")
def step(room_id):
    cli_step = int(request.args.get("step"))
    room = dict_room[room_id]
    req_step = {"change": 0}
    if cli_step < room.now_step:
        req_step['steps'] = room.steps[cli_step:]
        req_step["change"] = 1
        req_step['winner'] = room.winner
    return json.dumps(req_step)


# @app.route("/ready")
# def ready():

@app.route("/restart/<string:room_id>")
def restart_game(room_id):
    room = dict_room[room_id]
    room.reload()
    return "开始打扫战场"


@app.route("/")
def index():
    return render_template("/login.html")

@app.route('/login')
def login():
    dict_req = {'state':"No",'id':0}
    username = request.args.get('username')
    password = request.args.get("password")
    remember = request.args.get('remember')

    user = User.query.filter_by(username = username).first()
    if user==None:
        return jsonify(dict_req)
    if user.password == password:
        session['id'] = str(user.id)
        dict_req["state"] = "YES"
        dict_req["id"] = user.id
    return jsonify(dict_req)
    

@app.route("/roomlist/<string:id>")
def roomlist(id):
    if session['id'] == id:
        return render_template('/roomlist.html')
    else:
        flash("请登录后再进入")
        return render_template("/login.html")



@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    username = request.form.get('username')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    if not all([username,password,password2]):
        return "NO"
    if password2!=password:
        return
    if User.query.filter(User.username==username).count() != 0:
        return "No"
    user = User(username=username,password=password)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return "NO"
    return "YES"

if __name__ == '__main__':
    # 创建所有的表
    db.create_all()
    app.run(host="0.0.0.0", port=8080, debug=True)
