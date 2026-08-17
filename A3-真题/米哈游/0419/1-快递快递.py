import sys


# 计算一组数据的答案
def solve_case(points):
    # cnt1: x>=0, y>=0
    # cnt2: x<=0, y>=0
    # cnt3: x<=0, y<=0
    # cnt4: x>=0, y<=0
    cnt1 = cnt2 = cnt3 = cnt4 = 0

    for x, y in points:
        # 第一象限（含坐标轴）
        if x >= 0 and y >= 0:
            cnt1 += 1
        # 第二象限（含坐标轴）
        if x <= 0 and y >= 0:
            cnt2 += 1
        # 第三象限（含坐标轴）
        if x <= 0 and y <= 0:
            cnt3 += 1
        # 第四象限（含坐标轴）
        if x >= 0 and y <= 0:
            cnt4 += 1

    return max(cnt1, cnt2, cnt3, cnt4)


def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return

    t = int(data[0])
    idx = 1
    ans = []

    for _ in range(t):
        n = int(data[idx])
        idx += 1

        points = []
        for _ in range(n):
            x = int(data[idx])
            y = int(data[idx + 1])
            idx += 2
            points.append((x, y))

        ans.append(str(solve_case(points)))

    print("\n".join(ans))


if __name__ == "__main__":
    main()





# =====================================================

# 求取max(资源点的数量)

class Points:
    def __init__(self):

        self.p1 = 0
        self.p2 = 0
        self.p3 = 0
        self.p4 = 0

        return 

    def add(self, x, y):

        if x > 0 and y > 0:
            self.p1 += 1

        elif x < 0 and y > 0:
            self.p2 += 1

        elif x < 0 and y < 0:
            self.p3 += 1

        elif x > 0 and y < 0:
            self.p4 += 1

        # 然后考虑坐标轴上的点
        if x == 0:
            if y > 0:
                self.p1 += 1
                self.p4 += 1
            elif y < 0:
                self.p2 += 1
                self.p3 += 1

        if y == 0:
            if x > 0:
                self.p1 += 1
                self.p2 += 1
            elif x < 0:
                self.p3 += 1
                self.p4 += 1

        if x == 0 and y == 0:
            self.p1 += 1
            self.p2 += 1
            self.p3 += 1
            self.p4 += 1

    def max(self):
        return max(self.p1, self.p2, self.p3, self.p4)


def get_data():
    import sys

    all_datas = sys.stdin.read().split()
    ptr = 0

    T = int(all_datas[ptr])
    ptr += 1

    for t in range(T):
        n = int(all_datas[ptr])
        ptr += 1

        points = Points()
        for _ in range(n):
            x, y = int(all_datas[ptr]), int(all_datas[ptr + 1])
            ptr += 2

            points.add(x, y)

        print(points.max())

    return 


if __name__ == "__main__":
    main()

