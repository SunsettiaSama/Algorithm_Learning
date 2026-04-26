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
