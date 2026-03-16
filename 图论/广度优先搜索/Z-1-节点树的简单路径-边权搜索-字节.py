
"""

V0
彻底失败

"""


def get_input():
    import sys

    lines = sys.stdin.read().splitlines()

    n = int(lines[0])
    node_values = list(map(int, lines[1].split()))
    paths = []

    for _ in lines[2: ]:
        a, b = list(map(int, lines[1].split()))
        paths.append((a, b))
    
    return n, node_values, paths

# 哦，原来是边的意思，那就好说了啊

def search_nums():
    
    from collections import deque

    n, node_values, paths = get_input()

    queue = deque()
    queue.append(node_values)

    while queue:
         
        start_node, end_node = queue.popleft()
        # 判断两个条件

        # 1. 是否在路径上

        # 2. 如果在路径上，那么是否满足ax = ay的值

        # 但这里有一个问题我们没有处理过：如何对边进行广搜，我们都是对节点进行广搜的

    return 



"""
注意，这个是图论机考的一个重要问题，如何把边权值转化成邻接表以供dfs或者bfs

图-邻接表-回溯算法


"""

import sys
from collections import defaultdict

# ---------------------- 工具函数：计算组合数 C(n,2) ----------------------
# 作用：计算n个元素中选2个的组合数（无序对数量）
def comb2(n):
    if n < 2:
        return 0
    return n * (n - 1) // 2

# ---------------------- 步骤1：处理输入，转化为邻接表 ----------------------
def get_input():
    # 读取所有输入并拆分成数字列表（避免按行处理的坑）
    all_nums = sys.stdin.read().split()
    pointer = 0  # 指针：记录当前读到哪个数字
    
    # 第一步：读节点总数n
    node_count = int(all_nums[pointer])
    pointer += 1
    
    # 第二步：读每个节点的权值（节点1对应索引0，节点2对应索引1...）
    node_values = list(map(int, all_nums[pointer:pointer + node_count]))
    pointer += node_count
    
    # 第三步：构建邻接表（1-based，索引0不用）
    # adj[current_node] 存储和current_node相连的所有节点
    adjacency_list = [[] for _ in range(node_count + 1)]
    # 树有n-1条边，循环读n-1次
    for _ in range(node_count - 1):
        u = int(all_nums[pointer])    # 边的第一个节点
        v = int(all_nums[pointer+1])  # 边的第二个节点
        adjacency_list[u].append(v)   # 无向边：双向添加
        adjacency_list[v].append(u)
        pointer += 2
    
    return node_count, node_values, adjacency_list

# ---------------------- 步骤2：递归DFS遍历树，计算答案 ----------------------
def dfs(current_node, parent_node, node_values, adjacency_list, cnt, current_sum, ans):
    """
    递归DFS遍历树，维护路径状态并计算答案
    :param current_node: 当前遍历的节点
    :param parent_node: 父节点（避免走回头路）
    :param node_values: 所有节点的权值
    :param adjacency_list: 邻接表
    :param cnt: 字典，记录当前路径上各值的出现次数
    :param current_sum: 当前路径上符合条件的无序对总数
    :param ans: 结果数组，ans[i]存储节点i的答案
    """
    # 1. 拿到当前节点的权值（节点编号是1-based，数组是0-based）
    current_val = node_values[current_node - 1]
    
    # 2. 记录更新前的计数（用于计算组合数增量）
    old_count = cnt[current_val]
    
    # 3. 更新当前值的计数：当前路径上多了一个该值的节点
    cnt[current_val] += 1
    
    # 4. 计算组合数增量：新的组合数 - 旧的组合数
    new_comb = comb2(cnt[current_val])
    old_comb = comb2(old_count)
    current_sum += (new_comb - old_comb)
    
    # 5. 记录当前节点的答案（此时current_sum就是1→current_node路径的答案）
    ans[current_node] = current_sum
    
    # 6. 遍历当前节点的所有邻居（递归访问子节点）
    for neighbor in adjacency_list[current_node]:
        # 跳过父节点，避免走回头路（保证路径是1→current_node→neighbor）
        if neighbor != parent_node:
            # 递归访问子节点，传递更新后的状态
            dfs(neighbor, current_node, node_values, adjacency_list, cnt, current_sum, ans)
    
    # 7. 回溯：离开当前节点时，恢复状态（不影响其他分支的遍历）
    cnt[current_val] -= 1
    # 如果计数归0，删除键（节省空间，可选）
    if cnt[current_val] == 0:
        del cnt[current_val]

# ---------------------- 主函数：整合所有逻辑 ----------------------
def main():
    # 步骤1：读取输入
    node_count, node_values, adjacency_list = get_input()
    
    # 初始化：结果数组（1-based）
    ans = [0] * (node_count + 1)
    
    # 初始化：记录路径上各值的出现次数（默认值0）
    value_count = defaultdict(int)
    
    # 步骤2：从根节点1开始DFS（父节点设为-1，表示没有父节点）
    dfs(current_node=1, 
        parent_node=-1, 
        node_values=node_values, 
        adjacency_list=adjacency_list, 
        cnt=value_count, 
        current_sum=0, 
        ans=ans)
    
    # 步骤3：输出结果（节点1到节点n的答案）
    print(' '.join(map(str, ans[1:node_count+1])))

# 程序入口
if __name__ == "__main__":
    main()
