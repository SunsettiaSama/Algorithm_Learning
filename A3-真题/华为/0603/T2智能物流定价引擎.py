
# ========================= 最小二乘法 =========================
# ========================== 在线学习 ==========================

class Engine:
    def __init__(self):
        self.sx = 0
        self.sy = 0
        self.sxx = 0
        self.sxy = 0
        self.n = 0

    def add(self, x, y):
        self.sx += x
        self.sy += y
        self.sxx += x ** 2
        self.sxy += x * y
        self.n += 1

    def query(self, x):
        if self.n == 0:
            print("0.000000")
            return 
        try:
            a = (self.n * self.sxy - self.sx * self.sy) / (self.n * self.sxx - self.sx ** 2)
        except: 
            a = 0

        try:
            b = (self.sy - a * self.sx) / self.n
        except:
            b = 0

        print(f"{a * x + b:.6f}")

import sys

def solve():

    all_datas = sys.stdin.read().split()
    ptr = 0

    o_nums = int(all_datas[ptr])
    ptr += 1

    engine = Engine()

    for o_idx in range(o_nums):

        key = all_datas[ptr]
        ptr += 1

        if key == "ADD":
            x, y = int(all_datas[ptr]), int(all_datas[ptr + 1])
            ptr += 2

            engine.add(x, y)
        elif key == "QUERY":
            x = int(all_datas[ptr])
            ptr += 1
            engine.query(x)


if __name__ == "__main__":
    solve()

