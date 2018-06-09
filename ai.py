import random

source_map = []


def initMap():
    global source_map
    source_map = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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


def getBestMove(ponsition, color):
    global source_map
    initMap()
    getALLSource(ponsition)
    maxSource = 0
    list_max = []
    for i in range(15):
        for j in range(15):
            if ponsition[i][j] == 0:
                if maxSource < source_map[i][j]:
                    list_max = []
                    list_max.append([i, j])
                    maxSource = source_map[i][j]
                elif maxSource == source_map[i][j]:
                    list_max.append([i, j])
    rand_num = random.randint(0, len(list_max) - 1)
    for value in source_map:
        print(value)
    return list_max[rand_num]


def isLimit(line, row, x, y, i):
    if (line + i * y) >= 0 and (row + i * x) >= 0 and (line + i * y) < 15 and (row + i * x) < 15:
        return True
    return False


def aiUnDromp(line, row, color):
    global ponsition
    ponsition[line][row] = color


def aiDrimp(line, row, color):
    global ponsition
    ponsition[line][row] = 0


def getMaxSource(level, steps, ponsition, color):
    if level == 0:
        return 0
    global source_map
    getALLSource(ponsition, 1)
    maxSource = 0
    list_max = []
    for i in range(15):
        for j in range(15):
            if ponsition[i][j] == 0:
                if maxSource < source_map[i][j]:
                    list_max = []
                    list_max.append([i, j])
                    maxSource = source_map[i][j]
                elif maxSource == source_map[i][j]:
                    list_max.append([i, j])
    best_source = 0
    best_move = []
    for line, row in list_max:
        aiDrimp(line, row, color)
        min_source = best_source(level - 1, list_max, ponsition)
        aiUnDromp(line, row, color * -1)
        if best_source > min_source:
            best_move = []
            best_move.append([line, row])
            best_source = min_source
        elif min_source == 0:
            return [line, row]
        elif min_source != 0 and min_source == best_source:
            best_move.append([line, row])
    return best_move[0]


def getMinSource(level, steps, ponsition, color):
    if level == 0:
        return 0
    global source_map
    getALLSource(ponsition, -1)
    minSource = 0
    list_min = []
    for i in range(15):
        for j in range(15):
            if ponsition[i][j] == 0:
                if minSource < source_map[i][j]:
                    list_min = []
                    list_min.append([i, j])
                    minSource = source_map[i][j]
                elif minSource == source_map[i][j]:
                    list_min.append([i, j])
    best_source = 0
    best_move = []
    for line, row in list_min:
        aiDrimp(line, row, color)
        max_source = getMaxSource(level - 1, list_min, ponsition)
        aiUnDromp(line, row, color * -1)
        if best_source < max_source:
            best_move = []
            best_move.append([line, row])
            best_source = max_source
        elif max_source == 0:
            return [line, row]
        elif max_source != 0 and max_source == best_source:
            best_move.append([line, row])
    return best_move[0]


def getSource(empty_num, rob_num, man_num):
    source = 0
    if man_num == 1:
        source += 10
    elif man_num == 2:
        if empty_num:
            source += 200
        source += 60
    elif man_num == 3:
        if empty_num == 1:
            source += 1100
        if empty_num == 2:
            source += 2200
        source += 800
    elif man_num == 4:
        if empty_num == 1:
            source += 10000
        if empty_num == 2:
            source += 11000
        source += 12000
    elif man_num >= 5:
        source += 999999

    if rob_num == 0:
        source += 5
    elif rob_num == 1:
        source += 10
    elif rob_num == 2:
        if empty_num:
            source += 10
        source += 50
    elif rob_num == 3:
        if empty_num:
            source += 1000
        source += 600
    elif rob_num == 4:
        if empty_num:
            source += 10000
        source += 10000
    elif rob_num >= 5:
        source += 999999
    return source


def getRevSource(old_color, x, y, line, row, ponsition):
    """
    反向求参数
    :int old_color:
    :int x:
    :int y:
    :int line:
    :int row:
    :list[int][int] ponsition:
    :return:int
    """
    i = 1
    e = 0
    while (line - y * i) >= 0 and (row - x * i) >= 0 and (line - y * i) < 15 and (row - x * i) < 15:
        if ponsition[line - y * i][row - x * i] == old_color:
            i += 1
        else:
            if ponsition[line - y*i][row - x * i] == 0:
                e = 1
            break
    return [i-1, e]


def getALLSource(ponsition, self_color=-1):
    global source_map
    other_color = self_color*-1
    for line in range(15):
        for row in range(15):
            if ponsition[line][row] == 0:
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        empty_num = 0
                        rob_num = 0
                        man_num = 0
                        if not (x == 0 and y == 0):
                            # 当一个方向的颜色发生变化退出循环
                            old_color = 0
                            for i in range(1, 7):
                                if isLimit(line, row, x, y, i) == False:
                                    print(line, row, x, y, i, "L")
                                    break
                                print(line, row, x, y, i, "P")
                                num = ponsition[line + i * y][row + i * x]
                                if num == other_color:
                                    if old_color != 0 and num != old_color:
                                        rev_source = getRevSource(
                                            old_color, x, y, line, row, ponsition)
                                        if sum(rev_source) == 0:
                                            print(line, row)
                                            rob_num = 0 if rob_num < 3 else rob_num
                                        else:
                                            rob_num += rev_source[0]
                                            empty_num += rev_source[1]
                                        source_map[line][row] += getSource(
                                            empty_num, rob_num, man_num)
                                        break
                                    man_num += 1
                                    old_color = num
                                elif num == 0:
                                    empty_num += 1
                                    if old_color != 0:
                                        if old_color == other_color:
                                            rev_source = getRevSource(
                                                old_color, x, y, line, row, ponsition)
                                            man_num += rev_source[0]
                                            empty_num += rev_source[1]
                                        elif old_color == self_color:
                                            rev_source = getRevSource(
                                                old_color, x, y, line, row, ponsition)
                                            rob_num += rev_source[0]
                                            empty_num += rev_source[1]
                                    source_map[line][row] += getSource(
                                        empty_num, rob_num, man_num)
                                    break
                                elif num == self_color:
                                    if old_color != 0 and num != old_color:
                                        rev_source = getRevSource(
                                            old_color, x, y, line, row, ponsition)
                                        if sum(rev_source) == 0:
                                            man_num = 0 if man_num < 3 else man_num
                                            print(line, row)
                                        else:
                                            man_num += rev_source[0]
                                            empty_num += rev_source[1]
                                        source_map[line][row] += getSource(
                                            empty_num, rob_num, man_num)
                                        break
                                    rob_num += 1
                                    old_color = num
                                else:
                                    break
