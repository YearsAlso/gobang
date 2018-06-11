import random
from room.Room import Room
class AI_Room(Room):
    def __init__(self,id,name="250号人工智障"):
        super().__init__(id,name)
        self.source_map = []
    
    def initMap(self,):
        self.source_map = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
    
    
    def getBestMove(self, color):
        self.initMap()
        self.getALLSource(self.ponsition)
        maxSource = 0
        list_max = []
        for i in range(15):
            for j in range(15):
                if self.ponsition[i][j] == 0:
                    if maxSource < self.source_map[i][j]:
                        list_max = []
                        list_max.append([i, j])
                        maxSource = self.source_map[i][j]
                    elif maxSource == self.source_map[i][j]:
                        list_max.append([i, j])
        rand_num = random.randint(0, len(list_max) - 1)
        # for value in self.source_map:
        #     print(value)
        return list_max[rand_num]
    
    
    def isLimit(self,line, row, x, y, i):
        if (line + i * y) >= 0 and (row + i * x) >= 0 and (line + i * y) < 15 and (row + i * x) < 15:
            return True
        return False
    
    
    def aiUnDromp(self,line, row, color):
        self.ponsition[line][row] = color
    
    
    def aiDrimp(self,line, row, color):
        self.ponsition[line][row] = 0

    
    def getSource(self,empty_num, rob_num, man_num):
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
    
    
    def getRevSource(self,old_color, x, y, line, row, ponsition):
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
    
    
    def getALLSource(self, self_color=-1):
        other_color = self_color*-1
        for line in range(15):
            for row in range(15):
                if self.ponsition[line][row] == 0:
                    for x in range(-1, 2):
                        for y in range(-1, 2):
                            empty_num = 0
                            rob_num = 0
                            man_num = 0
                            if not (x == 0 and y == 0):
                                # 当一个方向的颜色发生变化退出循环
                                old_color = 0
                                for i in range(1, 7):
                                    if self.isLimit(line, row, x, y, i) == False:
                                        #print(line, row, x, y, i, "L")
                                        break
                                    #print(line, row, x, y, i, "P")
                                    num = self.ponsition[line + i * y][row + i * x]
                                    if num == other_color:
                                        if old_color != 0 and num != old_color:
                                            rev_source = self.getRevSource(
                                                old_color, x, y, line, row, self.ponsition)
                                            if sum(rev_source) == 0:
                                                print(line, row)
                                                rob_num = 0 if rob_num < 3 else rob_num
                                            else:
                                                rob_num += rev_source[0]
                                                empty_num += rev_source[1]
                                            self.source_map[line][row] += self.getSource(
                                                empty_num, rob_num, man_num)
                                            break
                                        man_num += 1
                                        old_color = num
                                    elif num == 0:
                                        empty_num += 1
                                        if old_color != 0:
                                            if old_color == other_color:
                                                rev_source = self.getRevSource(
                                                    old_color, x, y, line, row, self.ponsition)
                                                man_num += rev_source[0]
                                                empty_num += rev_source[1]
                                            elif old_color == self_color:
                                                rev_source = self.getRevSource(
                                                    old_color, x, y, line, row, self.ponsition)
                                                rob_num += rev_source[0]
                                                empty_num += rev_source[1]
                                        self.source_map[line][row] += self.getSource(
                                            empty_num, rob_num, man_num)
                                        break
                                    elif num == self_color:
                                        if old_color != 0 and num != old_color:
                                            rev_source = self.getRevSource(
                                                old_color, x, y, line, row, self.ponsition)
                                            if sum(rev_source) == 0:
                                                man_num = 0 if man_num < 3 else man_num
                                                print(line, row)
                                            else:
                                                man_num += rev_source[0]
                                                empty_num += rev_source[1]
                                            self.source_map[line][row] += self.getSource(
                                                empty_num, rob_num, man_num)
                                            break
                                        rob_num += 1
                                        old_color = num
                                    else:
                                        break
