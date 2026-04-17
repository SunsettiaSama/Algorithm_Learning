import sys
from typing import List, Tuple

def read_input() -> Tuple[int, int, List[int], List[int], List[int]]:
    """
    从标准输入读取全部数据，解析为：
    m: 需要的存储空间大小
    n: 候选张量个数
    sizes: 每个张量的大小列表
    swap_costs: 每个张量 swap 的代价列表
    recompute_costs: 每个张量重计算的代价列表
    """
    data = sys.stdin.read().strip().split()
    if not data:
        return None
    it = iter(data)
    m = int(next(it))
    n = int(next(it))
    sizes = [int(next(it)) for _ in range(n)]
    swap_costs = [int(next(it)) for _ in range(n)]
    recompute_costs = [int(next(it)) for _ in range(n)]
    return m, n, sizes, swap_costs, recompute_costs

def build_items(sizes: List[int], swap_costs: List[int], recompute_costs: List[int]) -> List[Tuple[int, int]]:
    """
    将每个张量转化为一个物品 (大小, 最小代价)
    最小代价 = min(swap代价, 重计算代价)
    """
    items = []
    for i in range(len(sizes)):
        size = sizes[i]
        min_cost = min(swap_costs[i], recompute_costs[i])
        items.append((size, min_cost))
    return items

def min_cost_to_meet_demand(items: List[Tuple[int, int]], m: int) -> int:
    """
    使用 0-1 背包动态规划求解达到至少 m 容量的最小代价
    返回最小代价，如果无法达到则返回一个很大的数（INF）
    """
    INF = 10**18
    # dp[j] 表示总容量恰好为 j 时的最小代价，j 从 0 到 m
    # 将所有超过 m 的容量压缩到 m
    dp = [INF] * (m + 1)
    dp[0] = 0  # 容量 0 的代价为 0

    for size, cost in items:
        # 倒序遍历保证每个物品只使用一次（0-1背包）
        for j in range(m, -1, -1):
            if dp[j] != INF:
                # 如果选择了当前物品，新容量 = j + size，但超过 m 的视为 m
                new_cap = j + size
                if new_cap > m:
                    new_cap = m
                # 尝试更新 dp[new_cap]
                if dp[new_cap] > dp[j] + cost:
                    dp[new_cap] = dp[j] + cost

    return dp[m]

def solve() -> None:
    """
    主函数：读取输入、处理、输出结果
    """
    # 1. 读取输入
    result = read_input()
    if result is None:
        return
    m, n, sizes, swap_costs, recompute_costs = result

    # 2. 构建物品列表（大小，最小代价）
    items = build_items(sizes, swap_costs, recompute_costs)

    # 3. 求解最小代价
    ans = min_cost_to_meet_demand(items, m)

    # 4. 输出结果
    INF = 10**18
    if ans == INF:
        print("error")
    else:
        print(ans)


"""
V0 临摹
"""
import sys
from typing import List, Tuple

def read_input() -> Tuple[int, int, List[int], List[int], List[int]]:

    data = sys.stdin.read().strip().split()
    if not data:
        return None
    it = iter(data)
    m = int(next(it))
    n = int(next(it))
    sizes = [int(next(it)) for _ in range(n)]
    swap_costs = [int(next(it)) for _ in range(n)]
    recompute_costs = [int(next(it)) for _ in range(n)]
    return m, n, sizes, swap_costs, recompute_costs

def build_items(sizes, swap_costs, recompute_costs):
    n = len(sizes)
    items = []
    for i in range(n):
        items.append((sizes[i], min(swap_costs[i], recompute_costs[i])))
    return items


def min_cost_to_meet_demand(items, m):
    # 0-1背包解该问题

    INF = 10e18
    # dp[j]定义:总容量 恰好 为j的最小总代价(价值),这个题目里面,超过的部分我们都给压缩到m上了
    dp = [INF for i in range(m + 1)]
    dp[0] = 0
    
    for size, cost in items:
        for j in range(m, -1, -1):
            if dp[j] != INF:
                new_cap = j + size
                if new_cap > m:
                    new_cap = m
                if dp[new_cap] > dp[j] + cost:
                    dp[new_cap] = dp[j] + cost

    return dp[m]

def solve():

    result = read_input()
    if result == None:
        print("error")
        return 
    
    m, n, sizes, swap_costs, recompute_costs = result

    items = build_items(sizes, swap_costs, recompute_costs)

    ans = min_cost_to_meet_demand(items, m)

    INF = 10**18
    if ans == INF:
        print("error")
    else:
        print(ans)
    


if __name__ == "__main__":
    solve()