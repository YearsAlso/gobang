from flask import Flask
from flask import render_template
from flask import request

import ai
import json

app = Flask(__name__)
winner = 65536
isAI = False

ponsition = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

now_step = 0
steps = [[]]

list_player = [0, 0]
Color = 1


def sourceSum(i, j, n=0):
    line_sum = sum(ponsition[i][j - 2:j + 3])
    
    row_sum = ponsition[i][j] + ponsition[i + 1][j] + ponsition[i + 2][j] + ponsition[i - 1][j] + ponsition[i - 2][
        j]
    left_sum = ponsition[i][j] + ponsition[i + 1][j + 1] + ponsition[i + 2][j + 2] + ponsition[i - 1][j - 1] + \
               ponsition[i - 2][j - 2]
    right_sum = ponsition[i][j] + ponsition[i + 1][j - 1] + ponsition[i + 2][j - 2] + ponsition[i - 1][j + 1] + \
                ponsition[i - 2][j + 2]
    
    return {0: [line_sum, row_sum, left_sum, right_sum], 1: line_sum, 2: row_sum, 3: left_sum, 4: right_sum}.get(n)


def isWinnerCore():
    for i in range(2, 13):
        for j in range(2, 13):
            if ponsition[i][j] != 0:
                line_sum = sum(ponsition[i][j - 2:j + 3])
                if line_sum == 5:
                    return 1
                elif line_sum == -5:
                    return -1
                
                row_sum = ponsition[i][j] + ponsition[i + 1][j] + ponsition[i + 2][j] + ponsition[i - 1][j] + \
                          ponsition[i - 2][j]
                if row_sum == 5:
                    return 1
                elif row_sum == -5:
                    return -1
                
                left_sum = ponsition[i][j] + ponsition[i + 1][j + 1] + ponsition[i + 2][j + 2] + ponsition[i - 1][
                    j - 1] + ponsition[i - 2][j - 2]
                if left_sum == 5:
                    return 1
                elif left_sum == -5:
                    return -1
                
                right_sum = ponsition[i][j] + ponsition[i + 1][j - 1] + ponsition[i + 2][j - 2] + ponsition[i - 1][
                    j + 1] + ponsition[i - 2][j + 2]
                if right_sum == 5:
                    return 1
                elif right_sum == -5:
                    return -1
    
    return 0


def isWinner(iLine, iRow, iColor):
    global Color, ponsition, list_player
    if Color != iColor and isAI==False:
        return 65536
    if (ponsition[iLine][iRow] != 0):
        return 65535
    if sum(list_player) != 2 and isAI==False:
        return 65534
    ponsition[iLine][iRow] = iColor
    Color = 1 if (Color == -1) else -1
    return isWinnerCore()


@app.route('/')
def index():
    return render_template('gobang.html')

@app.route('/AI')
def AI():
    global isAI,list_player
    list_player[1] = 1
    
    #return render_template('index.html')
    return render_template('gobangAI.html')


@app.route("/dromp")
def dromp():
    global now_step, steps, winner
    line = int(request.args.get("line"))
    rows = int(request.args.get("row"))
    color = int(request.args.get("color"))
    winner = isWinner(line, rows, color)
    if winner < 65534:
        now_step += 1
    steps.append([line, rows, color])
    dict_req = {"winner": winner, "line": line, "rows": rows, "color": color, "step": now_step}
    return json.dumps(dict_req)


@app.route("/drompAI")
def drompAI():
    global now_step, steps, winner,ponsition,isAI
    isAI = True
    line = int(request.args.get("line"))
    rows = int(request.args.get("row"))
    color = int(request.args.get("color"))
    winner = isWinner(line, rows, color)
    if winner >= 65534:
        winner = 0
    # steps.append([line, rows, color])
    dict_req = {"winner": winner, "line": [line], "rows": [rows]}
    ai_list = ai.getBestMove(ponsition,color*-1)
    dict_req["line"].append(ai_list[0])
    dict_req["rows"].append(ai_list[1])
    if winner==0:
        winner = isWinner(ai_list[0], ai_list[1], color*-1)
        dict_req["winner"] = winner
    return json.dumps(dict_req)


@app.route("/player")
def player():
    global list_player
    num = int(request.args.get("player"))
    if list_player[num]:
        return "NO"
    list_player[num] = 1
    return "YES"


@app.route("/step")
def step():
    global steps
    cli_step = int(request.args.get("step"))
    req_step = {"change": 0}
    if cli_step < now_step:
        req_step['steps'] = steps[cli_step:]
        req_step["change"] = 1
        req_step['winner'] = winner
    return json.dumps(req_step)


# @app.route("/ready")
# def ready():

@app.route("/restart")
def restart_game():
    global winner, ponsition, now_step, steps, Color
    winner = 65536
    ponsition = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    now_step = 0
    steps = [[]]
    Color = 1
    return "开始打扫战场"


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080,debug=True)
