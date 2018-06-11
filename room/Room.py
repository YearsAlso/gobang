class Room(object):
    def __init__(self,id,name="猪一样的对手"):
        self.name = name
        self.id = id
        self.winner = 65536
        self.isAI = False

        self.ponsition = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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

        self.now_step = 0
        self.steps = [[]]

        self.list_player = [0, 0]
        self.Color = 1
        
    def reload(self):
        self.winner = 65536
        self.isAI = False
    
        self.ponsition = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
    
        self.now_step = 0
        self.steps = [[]]
    
        self.list_player = [0, 0]
        self.Color = 1
        
    def isFull(self):
        if sum(self.list_player) == 2:
            return True
        return False

    def sourceSum(self,i, j, n=0):
        line_sum = sum(self.ponsition[i][j - 2:j + 3])
    
        row_sum = self.ponsition[i][j] + self.ponsition[i + 1][j] + self.ponsition[i + 2][j] + self.ponsition[i - 1][j] + self.ponsition[i - 2][
            j]
        left_sum = self.ponsition[i][j] + self.ponsition[i + 1][j + 1] + self.ponsition[i + 2][j + 2] + self.ponsition[i - 1][j - 1] + \
                   self.ponsition[i - 2][j - 2]
        right_sum = self.ponsition[i][j] + self.ponsition[i + 1][j - 1] + self.ponsition[i + 2][j - 2] + self.ponsition[i - 1][j + 1] + \
                    self.ponsition[i - 2][j + 2]
    
        return {0: [line_sum, row_sum, left_sum, right_sum], 1: line_sum, 2: row_sum, 3: left_sum, 4: right_sum}.get(n)

    def isWinnerCore(self):
        for i in range(2, 13):
            for j in range(2, 13):
                if self.ponsition[i][j] != 0:
                    line_sum = sum(self.ponsition[i][j - 2:j + 3])
                    if line_sum == 5:
                        return 1
                    elif line_sum == -5:
                        return -1
                
                    row_sum = self.ponsition[i][j] + self.ponsition[i + 1][j] + self.ponsition[i + 2][j] + self.ponsition[i - 1][j] + \
                              self.ponsition[i - 2][j]
                    if row_sum == 5:
                        return 1
                    elif row_sum == -5:
                        return -1
                
                    left_sum = self.ponsition[i][j] + self.ponsition[i + 1][j + 1] + self.ponsition[i + 2][j + 2] + self.ponsition[i - 1][
                        j - 1] + self.ponsition[i - 2][j - 2]
                    if left_sum == 5:
                        return 1
                    elif left_sum == -5:
                        return -1
                
                    right_sum = self.ponsition[i][j] + self.ponsition[i + 1][j - 1] + self.ponsition[i + 2][j - 2] + self.ponsition[i - 1][
                        j + 1] + self.ponsition[i - 2][j + 2]
                    if right_sum == 5:
                        return 1
                    elif right_sum == -5:
                        return -1
    
        return 0

    def isWinner(self,iLine, iRow, iColor):
        if self.Color != iColor and self.isAI == False:
            return 65536
        if (self.ponsition[iLine][iRow] != 0):
            return 65535
        if sum(self.list_player) != 2 and self.isAI == False:
            return 65534
        self.ponsition[iLine][iRow] = iColor
        self.Color = 1 if (self.Color == -1) else -1
        return self.isWinnerCore()
