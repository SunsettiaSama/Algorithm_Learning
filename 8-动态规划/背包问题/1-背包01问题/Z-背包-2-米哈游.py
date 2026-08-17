from typing import List, Tuple, Set, Dict

# ------------------------------------------------------------
# 模块1：提取所有参与互斥关系的物品编号
# ------------------------------------------------------------
def extract_conflict_items(n: int, conflicts: List[Tuple[int, int]]) -> List[int]:
    """
    从互斥对中收集所有出现过的物品编号，去重后返回列表。
    """
    conflict_set = set()
    for a, b in conflicts:
        conflict_set.add(a)
        conflict_set.add(b)
    return list(conflict_set)

# ------------------------------------------------------------
# 模块2：分离无冲突物品（不在冲突集合中的物品）
# ------------------------------------------------------------
def get_rest_items(n: int, weights: List[int], values: List[int], conflict_set: Set[int]) -> List[Tuple[int, int]]:
    """
    返回所有不在 conflict_set 中的物品，每个物品表示为 (重量, 价值)
    """
    rest = []
    for i in range(1, n + 1):
        if i not in conflict_set:
            rest.append((weights[i], values[i]))
    return rest

# ------------------------------------------------------------
# 模块3：普通0-1背包预处理（无冲突物品）
# ------------------------------------------------------------
def knapsack_rest(items: List[Tuple[int, int]], capacity: int) -> List[int]:
    """
    对 items 列表（无冲突）进行0-1背包DP，返回 dp 数组，dp[c] 表示容量 c 能获得的最大价值。
    """
    dp = [0] * (capacity + 1)
    for w, v in items:
        for c in range(capacity, w - 1, -1):
            if dp[c - w] + v > dp[c]:
                dp[c] = dp[c - w] + v
    return dp

# ------------------------------------------------------------
# 模块4：枚举冲突子集，结合预处理背包求解最大价值
# ------------------------------------------------------------
def solve_with_small_conflict_set(n: int, m: int,
                                  weights: List[int],
                                  values: List[int],
                                  conflicts: List[Tuple[int, int]]) -> int:
    """
    主求解函数：假设参与互斥的物品数量 t 较小（如 t <= 20）。
    weights 和 values 是 1-indexed 列表（索引0未使用）。
    """
    # 步骤1：提取冲突物品列表
    conflict_list = extract_conflict_items(n, conflicts)
    t = len(conflict_list)
    conflict_set = set(conflict_list)

    # 步骤2：获取无冲突物品
    rest_items = get_rest_items(n, weights, values, conflict_set)

    # 步骤3：预处理无冲突物品的背包
    dp_rest = knapsack_rest(rest_items, m)

    # 步骤4：建立物品编号到其在 conflict_list 中索引的映射
    idx_map = {node: i for i, node in enumerate(conflict_list)}

    ans = 0
    # 枚举所有子集（mask 从 0 到 (1<<t)-1）
    for mask in range(1 << t):
        # 4.1 检查是否违反互斥关系
        ok = True
        for a, b in conflicts:
            ia = idx_map.get(a)
            ib = idx_map.get(b)
            if ia is not None and ib is not None:
                if ((mask >> ia) & 1) and ((mask >> ib) & 1):
                    ok = False
                    break
        if not ok:
            continue

        # 4.2 计算该子集的总重量和总价值
        total_w = 0
        total_v = 0
        for i in range(t):
            if (mask >> i) & 1:
                node = conflict_list[i]
                total_w += weights[node]
                total_v += values[node]
                if total_w > m:   # 剪枝：超重则无需继续
                    break
        if total_w > m:
            continue

        # 4.3 剩余容量由无冲突物品填充
        cur = total_v + dp_rest[m - total_w]
        if cur > ans:
            ans = cur

    return ans

# ------------------------------------------------------------
# 示例用法（若直接运行本文件）
# ------------------------------------------------------------
if __name__ == "__main__":
    # 测试数据
    n, m, k = 4, 10, 2
    weights = [0, 2, 3, 4, 5]   # 索引1~4
    values  = [0, 3, 4, 5, 6]
    conflicts = [(1, 2), (3, 4)]

    result = solve_with_small_conflict_set(n, m, weights, values, conflicts)
    print(f"最大价值: {result}") 
    