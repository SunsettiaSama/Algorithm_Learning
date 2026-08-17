


import sys
import numpy as np

class engine:
    def __init_(self, K):

        self.pos = np.array([], dtype = float)
        # 这个就是注意力分数
        self.score = np.array([], dtype = float)
        self.key = np.array([], dtype = float)
        self.value = np.array([], dtype = float)

        self.K = K

        return 


    def add(self, pos, score, key, value):

        # 如果数量不足，那么可以入列
        if len(self.pos) < self.K:
            self.pos.append(pos)
            self.score.append(score)
            self.key.append(key)
            self.value.append(value)

        # 需要排除注意力分数最低者
        else:
            # 检查该剪枝谁

            indices = self.score.argsort()
            # 剪去最小者，问题2，已知索引，该删什么内容
            abandon_index = indices[0]
            np.delete()
        

        return 


    def query(self):

        return 
    









def solve():

    all_datas = sys.stdin.read().split()
    ptr = 0

    K = int(all_datas[ptr])
    ptr += 1

    N = int(all_datas[ptr])
    ptr += 1

    pos = []
    scores = []
    keys = []
    values = []
    
    for _ in range(N):
        op = all_datas[ptr]
        ptr += 1

        if op == "ADD":



    

