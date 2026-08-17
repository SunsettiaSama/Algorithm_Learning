import sys
from functools import lru_cache

def read_input():
    data = sys.stdin.read().strip().split()
    it = iter(data)
    n = int(next(it))
    m = int(next(it))
    t = int(next(it))
    tasks = []
    for _ in range(n):
        a = int(next(it))
        b = int(next(it))
        c = int(next(it))
        d = int(next(it))
        tasks.append((a, b, c, d))
    return n, m, t, tasks

def dfs_solution(n, m, t, tasks):
    # 记忆化DFS：idx=当前第几个任务, used_m=已用token, used_t=已用时间
    @lru_cache(maxsize=None)
    def dfs(idx, used_m, used_t):
        # 边界：所有任务遍历完
        if idx == n:
            return 0
        
        # 选择1：不做当前任务
        res = dfs(idx + 1, used_m, used_t)
        
        a, b, c, d = tasks[idx]
        # 选择2：常规模式
        if used_m + a <= m and used_t + b <= t:
            res = max(res, 1 + dfs(idx + 1, used_m + a, used_t + b))
        # 选择3：降耗模式
        if used_m + c <= m and used_t + d <= t:
            res = max(res, 1 + dfs(idx + 1, used_m + c, used_t + d))
        
        return res
    
    return dfs(0, 0, 0)

def solve():
    n, m, t, tasks = read_input()
    print(dfs_solution(n, m, t, tasks))

if __name__ == "__main__":
    solve()



import sys

def read_input():
    """读取输入数据"""
    data = sys.stdin.read().strip().split()
    if not data:
        return None
    it = iter(data)
    n = int(next(it))
    m = int(next(it))
    t = int(next(it))
    tasks = []
    for _ in range(n):
        a = int(next(it))  # 常规模式token
        b = int(next(it))  # 常规模式时间
        c = int(next(it))  # 降耗模式token
        d = int(next(it))  # 降耗模式时间
        tasks.append((a, b, c, d))
    return n, m, t, tasks

def init_dp(m, t):
    """
    初始化DP数组
    dp[i][j] = 消耗i个token、j个时间时，能完成的最大任务数
    初始状态：只有(0,0)可达，任务数为0，其余为-1（不可达）
    """
    dp = [[-1] * (t + 1) for _ in range(m + 1)]
    dp[0][0] = 0
    return dp


def update_dp(dp, a, b, c, d, m, t):

    for i in range(m, -1, -1):
        for j in range(t, -1, -1):

            if dp[i][j] == -1:
                continue

            ni, nj = i + a, j + b
            if ni <= m and nj <= t:
                if dp[ni][nj] < dp[i][j] + 1:
                    dp[ni][nj] = dp[i][j] + 1

            ni, nj = i + c, j + d
            if ni <= m and nj <= t:
                if dp[ni][nj] > dp[i][j] + 1:
                    dp[ni][nj] = dp[i][j] + 1

def compute_max_tasks(dp, m, t):
    """遍历所有状态，计算最大可完成任务数"""
    max_count = 0
    for i in range(m + 1):
        for j in range(t + 1):
            if dp[i][j] > max_count:
                max_count = dp[i][j]
    return max_count

def solve():
    """主函数：串联所有模块"""
    input_data = read_input()
    if input_data is None:
        return
    n, m, t, tasks = input_data
    
    # 初始化DP
    dp = init_dp(m, t)
    
    # 逐个任务更新DP
    for a, b, c, d in tasks:
        update_dp(dp, a, b, c, d, m, t)
    
    # 计算结果
    result = compute_max_tasks(dp, m, t)
    print(result)

if __name__ == "__main__":
    solve()

