import sys
import math
from collections import defaultdict
import bisect

def build_sparse_table(arr):
    """构建稀疏表，支持区间最小值查询"""
    n = len(arr)
    log = [0] * (n + 1)
    for i in range(2, n + 1):
        log[i] = log[i // 2] + 1
    K = log[n] + 1
    st = [[0] * n for _ in range(K)]
    st[0] = arr[:]
    for k in range(1, K):
        step = 1 << (k - 1)
        for i in range(n - (1 << k) + 1):
            st[k][i] = min(st[k-1][i], st[k-1][i+step])
    return st, log

def query_min(st, log, l, r):
    """查询闭区间 [l, r] 的最小值，l, r 是下标（0-indexed）"""
    if l > r:
        return 10**18  # 空区间返回无穷大
    length = r - l + 1
    k = log[length]
    return min(st[k][l], st[k][r - (1 << k) + 1])

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        a = [int(next(it)) for _ in range(n)]
        # 构建位置映射
        pos = defaultdict(list)
        for idx, val in enumerate(a, start=1):  # 1-indexed 位置
            pos[val].append(idx)
        # 构建稀疏表（0-indexed 值）
        st, log = build_sparse_table(a)  # a 是 0-indexed 列表
        ans = 0
        for i in range(1, n+1):
            val = a[i-1]
            # 向右找 val+1
            tar = val + 1
            if tar in pos:
                lst = pos[tar]
                j_idx = bisect.bisect_right(lst, i)  # 第一个大于 i 的位置
                if j_idx < len(lst):
                    j = lst[j_idx]
                    # 查询区间 (i, j) 的最小值，对应下标 i 到 j-2（因为 a 是 0-indexed）
                    if i+1 <= j-1:
                        mn = query_min(st, log, i, j-2)  # 注意：i 和 j 是 1-indexed，转换为 0-indexed 需要减1
                        # 区间 [i, j-2] 对应原下标 i+1? 我们来仔细算：
                        # 原始位置 i (1-indexed) 对应数组下标 i-1
                        # 开区间 (i, j) 包含的位置是 i+1, i+2, ..., j-1
                        # 这些位置对应的数组下标是 i, i+1, ..., j-2
                        # 所以查询闭区间 [i, j-2] (0-indexed)
                        if mn > max(val, tar):
                            ans += 1
                    else:
                        # 相邻，区间为空
                        ans += 1
            # 向右找 val-1
            tar = val - 1
            if tar >= 1 and tar in pos:
                lst = pos[tar]
                j_idx = bisect.bisect_right(lst, i)
                if j_idx < len(lst):
                    j = lst[j_idx]
                    if i+1 <= j-1:
                        mn = query_min(st, log, i, j-2)
                        if mn > max(val, tar):
                            ans += 1
                    else:
                        ans += 1
        out.append(str(ans))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()