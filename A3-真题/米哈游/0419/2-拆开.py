import sys
from typing import List, Optional, Tuple

def parse_input() -> List[Tuple[int, int, int, int]]:
    """读取所有输入，返回测试用例列表，每个元素为 (n, k, m, r)"""
    data = sys.stdin.read().strip().split()
    if not data:
        return []
    it = iter(data)
    t = int(next(it))
    cases = []
    for _ in range(t):
        n = int(next(it)); k = int(next(it)); m = int(next(it)); r = int(next(it))
        cases.append((n, k, m, r))
    return cases

def construct_r_zero(n: int, k: int, m: int) -> Optional[List[int]]:
    """
    处理 r == 0 的情况。
    返回构造的 a 列表（正整数），若不可行则返回 None。
    """
    if n % m != 0:
        return None
    S = n // m                     # sum of x_i
    min_sum = k * (k + 1) // 2     # 1+2+...+k
    if S < min_sum:
        return None
    # 构造 x_i = 1,2,...,k
    x = list(range(1, k + 1))
    d = S - min_sum
    x[-1] += d
    # 转换回 a_i = m * x_i
    return [m * xi for xi in x]

def construct_r_positive(n: int, k: int, m: int, r: int) -> Optional[List[int]]:
    """
    处理 r > 0 的情况。
    返回构造的 a 列表（正整数），若不可行则返回 None。
    """
    if n < k * r:
        return None
    diff = n - k * r
    if diff % m != 0:
        return None
    S = diff // m
    min_sum = k * (k - 1) // 2     # 0+1+...+(k-1)
    if S < min_sum:
        return None
    # 构造 x_i = 0,1,...,k-1
    x = list(range(k))
    d = S - min_sum
    x[-1] += d
    # 转换回 a_i = r + m * x_i
    return [r + m * xi for xi in x]

def process_case(n: int, k: int, m: int, r: int) -> Tuple[str, Optional[List[int]]]:
    """ 处理单个测试用例，返回 (状态, 列表) 状态为 "YES" 或 "NO" """
    if r == 0:
        res = construct_r_zero(n, k, m)
    else:
        res = construct_r_positive(n, k, m, r)
    if res is None:
        return ("NO", None)
    else:
        return ("YES", res)

def format_output(results: List[Tuple[str, Optional[List[int]]]]) -> str:
    """将结果列表格式化为输出字符串"""
    lines = []
    for status, arr in results:
        lines.append(status)
        if status == "YES":
            lines.append(" ".join(str(x) for x in arr))
    return "\n".join(lines)

def solve() -> None:
    cases = parse_input()
    results = []
    for n, k, m, r in cases:
        results.append(process_case(n, k, m, r))
    sys.stdout.write(format_output(results))



import sys

def solve(n, k, m, r):

    if n < k * r:
        print("NO")
        return
    if (n - k * r) % m != 0:
        print("NO")
        return
    
    
    # ci = L, L + 1, ..., L + k - 1
    if r == 0:
        L = 1
    else:
        L = 0

    delta = (n - k * r ) // m - (k * L + k * (k - 1) // 2)

    if delta < 0:
        print("NO")
        return 
    
    c = [i + L for i in range(k - 1)]
    c.append(L + k - 1 + delta)
    a = [r + m * ci for ci in c]

    print("YES")
    print(" ".join([str(ai) for ai in a]))

    return 


def get_input():

    lines = sys.stdin.read().split()
    ptr = 0

    T = int(lines[0])
    ptr += 1

    cases = []
    for t in range(T):
        n, k, m, r = list(map(int, lines[ptr: ptr + 4]))
        cases.append((n, k, m, r))
        ptr += 4
    
    return T, cases

def main():
    T, cases = get_input()
    for case in cases:
        solve(*case)


if __name__ == "__main__":
    main()




# ===================================================

# 主要问题：重要问题
# 推导中如何理解Smin
import sys

def solve(N, K, M, R):

    if (N - K * R) % M != 0: # 问题：不可除零，且要求S计算结果为整数
        return (-1, None)
    
    S = (N - K * R) // M # 问题二，浮点数除法
    if S < 0: # 问题三，边界条件，S = 0存在合法解
        return (-1, None)

    if R == 0:
        Smin = K * (K + 1) // 2 # 问题二，浮点数除法
        start_idx = 1
    else:
        Smin = K * (K - 1) // 2
        start_idx = 0

    delta = S - Smin

    if delta < 0:
        return (-1, None)

    
    # 此时成立，则以最小值进行构筑
    ans = []
    for i in range(start_idx, start_idx + K - 1): # 问题四，这里因为忘记start_idx会压缩区间了，R = 0时会缺答案
        ans.append(i * M + R)

    ans.append((start_idx + K - 1 + delta) * M + R) # 问题五，上面忘记改，这里跟着一起错了

    return (1, ans)


def main():


    all_datas = sys.stdin.read().split()
    ptr = 0 


    T = int(all_datas[ptr])
    ptr += 1

    for t in range(T): # 问题一，忘记range
        N, K, M, R = int(all_datas[ptr]), int(all_datas[ptr + 1]), int(all_datas[ptr + 2]), int(all_datas[ptr + 3]) # 问题五,忘记了指针的写法, 以后干脆用迭代器吧
        ptr += 4

        ans_tuple = solve(N, K, M, R)
        if ans_tuple[0] == -1:
            sys.stdout.write("NO\n") 
        else:
            sys.stdout.write("YES\n") 
            ans = ans_tuple[1]
            print(" ".join([str(item) for item in ans]), end = "\n" if not t == T - 1 else "") # 问题六,最后一行总是会默认换行,该如何解决


if __name__ == "__main__":
    main()
