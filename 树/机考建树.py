

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












