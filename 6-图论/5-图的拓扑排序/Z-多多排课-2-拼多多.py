

import sys


# 计算最少需要多少个学期
def min_semesters(n, parent):
    # memo[i] 表示课程 i 的深度（也就是最早可安排的学期）
    memo = [0] * (n + 1)

    # 记忆化递归计算课程 x 的深度
    def get_depth(x):
        # 如果已经计算过，直接返回
        if memo[x] != 0:
            return memo[x]

        # 没有先修课，深度为 1
        if parent[x] == -1:
            memo[x] = 1
        else:
            # 否则深度等于直接先修课深度 + 1
            memo[x] = get_depth(parent[x]) + 1
        return memo[x]

    ans = 0
    for i in range(1, n + 1):
        ans = max(ans, get_depth(i))
    return ans


def main():
    input = sys.stdin.readline
    n = int(input().strip())

    # parent[i] 表示课程 i 的直接先修课
    parent = [0] * (n + 1)
    for i in range(1, n + 1):
        parent[i] = int(input().strip())

    print(min_semesters(n, parent))




"""
V1手搓


总的来说,这个题目可以用树来解决,但是走了弯路,最好用链表来做

"""

# 计算最少需要多少个学期
def min_semesters(n, parent):
    # memo[i] 表示课程 i 的深度（也就是最早可安排的学期）
    memo = [0] * (n + 1)

    def get_depth(x):
        if memo[x] != 0:
            return memo[x]
        
        if parent[x] == -1:
            memo[x] = 1

        else:
            memo[x] = get_depth(parent[x]) + 1
        
        return memo[x]
    
    ans = 0
    for i in range(1, n + 1):
        ans = max(ans, get_depth(i))

    return ans


def main():
    input = sys.stdin.readline
    n = int(input().strip())

    # parent[i] 表示课程 i 的直接先修课
    parent = [0] * (n + 1)
    for i in range(1, n + 1):
        parent[i] = int(input().strip())

    print(min_semesters(n, parent))



"""
kahn算法,DAG

"""

from collections import deque

def build_graph_and_indegree(n, parent):
    """建图：邻接表 + 入度统计"""
    graph = [[] for _ in range(n + 1)]
    indegree = [0] * (n + 1)
    for v in range(1, n + 1):
        u = parent[v]
        if u != -1:
            graph[u].append(v)
            indegree[v] += 1
    return graph, indegree

def init_queue_and_semester(n, indegree):
    """初始化队列（入度为0的节点）和 semester 数组"""
    q = deque()
    semester = [0] * (n + 1)
    for v in range(1, n + 1):
        if indegree[v] == 0:
            q.append(v)
            semester[v] = 1
    return q, semester

def bfs_topological_sort(n, graph, indegree, q, semester):
    """BFS 拓扑排序，计算每门课程的最早学期"""
    while q:
        u = q.popleft()
        for v in graph[u]:
            semester[v] = max(semester[v], semester[u] + 1)
            indegree[v] -= 1
            if indegree[v] == 0:
                q.append(v)
    # 可选：检测环（如果还有节点入度>0，则存在环，但题目保证无环）
    return semester

def min_semesters_kahn(n, parent):
    """Kahn 算法主函数"""
    graph, indegree = build_graph_and_indegree(n, parent)
    q, semester = init_queue_and_semester(n, indegree)
    semester = bfs_topological_sort(n, graph, indegree, q, semester)
    return max(semester[1:])

def main():
    import sys
    data = sys.stdin.read().strip().split()
    if not data:
        return
    n = int(data[0])
    parent = [0] * (n + 1)
    for i in range(1, n + 1):
        parent[i] = int(data[i])
    print(min_semesters_kahn(n, parent))

"""
DFS版本

"""


def dfs_topological(u, graph, visited, stack, in_stack):
    """
    递归 DFS，检测环并收集后序顺序
    返回 True 表示无环，False 表示有环
    """
    visited[u] = 1          # 正在访问
    in_stack[u] = True
    for v in graph[u]:
        if visited[v] == 0:
            if not dfs_topological(v, graph, visited, stack, in_stack):
                return False
        elif in_stack[v]:   # 发现环
            return False
    visited[u] = 2          # 已完成
    in_stack[u] = False
    stack.append(u)
    return True

def min_semesters_dfs_general(n, parent):
    # 建图（支持多先修课，但这里输入是单父节点）
    graph = [[] for _ in range(n + 1)]
    indegree = [0] * (n + 1)
    for v in range(1, n + 1):
        u = parent[v]
        if u != -1:
            graph[u].append(v)
            indegree[v] += 1

    # DFS 获得拓扑序（逆序）
    visited = [0] * (n + 1)
    in_stack = [False] * (n + 1)
    stack = []
    for v in range(1, n + 1):
        if visited[v] == 0:
            if not dfs_topological(v, graph, visited, stack, in_stack):
                raise Exception("图中存在环，无法拓扑排序")
    topo_order = stack[::-1]   # 正向拓扑序

    # 按拓扑序 DP 求最长路径（学期数）
    dist = [1] * (n + 1)       # 至少为1
    for u in topo_order:
        for v in graph[u]:
            dist[v] = max(dist[v], dist[u] + 1)
    return max(dist[1:])

def main():
    import sys
    data = sys.stdin.read().strip().split()
    if not data:
        return
    n = int(data[0])
    parent = [0] * (n + 1)
    for i in range(1, n + 1):
        parent[i] = int(data[i])
    print(min_semesters_dfs_general(n, parent))

if __name__ == "__main__":
    main()

    