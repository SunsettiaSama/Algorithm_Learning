



# 专家路由，E个专家

# 每个专家的最大容量为C

# 对于每一个Token，会给每个专家打分，将Token分配给得分排名前K的专家


import sys
import numpy as np


def get_data():

    all_datas = sys.stdin.read().split()
    ptr = 0

    N, E, K, C = int(all_datas[ptr]), int(all_datas[ptr + 1]), int(all_datas[ptr + 2]), int(all_datas[ptr + 3])
    ptr += 4

    S = []
    for _ in range(N):
        s = [int(all_datas[ptr + i]) for i in range(E)]
        S.append(s)
        ptr += E


    return N, E, K, C, S

def solve():


    N, E, K, C, S = get_data()

    # 裁取前C个专家
    # 问题一
    # 问题二
    M = np.argsort(-np.array(S, dtype = int), kind = 'stable', axis = 1)[:, :K]

    loads = np.zeros(shape = (E, ), dtype = int)
    for e_row in M:
        for e in e_row:
            if loads[e] < C:
                loads[e] += 1

    # 问题三
    print(str(np.sum(np.square(loads))))
    print(' '.join([str(load) for load in loads]))
    


if __name__ == "__main__":
    solve()