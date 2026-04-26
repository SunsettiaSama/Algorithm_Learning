import sys


def solve_case(a):
    # 单调递增栈
    stack = []
    ans = 0

    for x in a:
        # 弹出所有比当前值大的元素
        while stack and stack[-1] > x:
            # 若差值为 1，则形成合法数对
            if stack[-1] == x + 1:
                ans += 1
            stack.pop()

        # 弹栈结束后，若栈顶恰好是 x - 1，也能形成合法数对
        if stack and stack[-1] == x - 1:
            ans += 1

        # 维护严格递增栈
        if not stack or stack[-1] < x:
            stack.append(x)
        # 若栈顶等于当前值，则不需要入栈

    return ans


def main():
    data = list(map(int, sys.stdin.read().split()))
    t = data[0]
    idx = 1
    res = []

    for _ in range(t):
        n = data[idx]
        idx += 1
        a = data[idx:idx + n]
        idx += n
        res.append(str(solve_case(a)))

    print("\n".join(res))


if __name__ == "__main__":
    main()
