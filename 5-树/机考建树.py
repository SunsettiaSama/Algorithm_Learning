

# 邻接表
import sys
from collections import defaultdict

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




"""
注意，树是有向图，有根节点

一定是从根节点向下递归

"""

import sys  # 1. 必须加这个！

# ---------------------- 步骤1：处理输入，转化为邻接表 ----------------------
def get_input():
    all_nums = sys.stdin.read().split()  # 用这个最稳，不踩换行的坑
    ptr = 0

    # 读节点数量
    n = int(all_nums[ptr])
    ptr += 1

    # 读节点权值
    values = []
    for i in range(n):
        values.append(int(all_nums[ptr]))
        ptr += 1

    # 2. 建表：节点从1开始，所以列表长度 n+1
    adj = [[] for i in range(n + 1)]

    # 3. 树固定有 n-1 条边
    for i in range(n - 1):
        u = int(all_nums[ptr])
        v = int(all_nums[ptr+1])
        # 4. 无向边：双向添加！
        adj[u].append(v)
        adj[v].append(u)
        ptr += 2

    return n, values, adj



# ---------------------- 你要的主接口！核心就在这 ----------------------
if __name__ == "__main__":
    print("===== 程序开始运行 =====")
    
    # 调用输入函数，拿到所有数据
    n, values, adj = get_input()
    
    # 打印结果，验证对不对（大爷你看这里就行）
    print(f"节点总数：{n}")
    print(f"每个节点的权值：{values}")
    print(f"树的邻接表：{adj}")
    
    print("===== 程序运行结束 =====")










