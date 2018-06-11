from flask import Flask, jsonify
from flask import render_template
from flask import request
from room.Room import Room
from room.AI import AI_Room

import ai
import json
import random
import time

app = Flask(__name__)
dict_room = {}


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
    ai_list = ai.getBestMove(room.ponsition, color * -1)
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
    return render_template("/list.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
